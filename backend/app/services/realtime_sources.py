from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
from xml.etree import ElementTree
import asyncio

import httpx

from app.schemas.api import RiskFeatures
from app.services.recommendations import build_recommendation
from app.services.risk_model import CrisisRiskModel, classify_category, severity_from_score
from app.services.top_cities import CITY_BY_CODE, TOP_50_CITIES, CityBaseline

WEATHER_TIMEOUT = 8.0
NEWS_TIMEOUT = 10.0
NEGATIVE_TERMS = {
    "crisis",
    "crime",
    "murder",
    "violence",
    "riot",
    "protest",
    "flood",
    "heatwave",
    "drought",
    "unemployment",
    "inflation",
    "shortage",
    "strike",
    "pollution",
    "accident",
    "disease",
}
POSITIVE_TERMS = {"growth", "jobs", "investment", "rain", "relief", "development", "recovery", "peace", "improvement"}


class RealtimeDataError(RuntimeError):
    pass


class RealtimeCityService:
    def __init__(self) -> None:
        self.model = CrisisRiskModel()

    async def top50(self, limit: int = 50) -> list[dict]:
        cities = TOP_50_CITIES[: max(1, min(limit, 50))]
        async with httpx.AsyncClient(headers={"User-Agent": "CrisisIQ/1.0"}) as client:
            semaphore = asyncio.Semaphore(8)

            async def fetch(city: CityBaseline) -> dict:
                async with semaphore:
                    return await self.city_risk(city.code, client=client)

            return await asyncio.gather(*(fetch(city) for city in cities))

    async def city_risk(self, code: str, client: httpx.AsyncClient | None = None) -> dict:
        city = CITY_BY_CODE.get(code.upper())
        if not city:
            raise RealtimeDataError(f"Unknown city code: {code}")

        owns_client = client is None
        active_client = client or httpx.AsyncClient(headers={"User-Agent": "CrisisIQ/1.0"})
        try:
            weather = await self._weather(city, active_client)
            news = await self._news(city, active_client)
        finally:
            if owns_client:
                await active_client.aclose()

        features = self._build_features(city, weather, news)
        risk_score, probability, drivers = self.model.predict(features)
        category = classify_category(drivers)
        severity = severity_from_score(risk_score)
        recommendation = build_recommendation(city.code, category, risk_score)

        return {
            "code": city.code,
            "city": city.city,
            "state": city.state,
            "latitude": city.latitude,
            "longitude": city.longitude,
            "population_millions": city.population_millions,
            "risk_score": risk_score,
            "probability": probability,
            "severity": severity,
            "category": category,
            "drivers": drivers,
            "recommendation": recommendation.model_dump(),
            "features": features.model_dump(),
            "live": {
                "weather": weather,
                "news": news,
            },
            "sources": [
                "Open-Meteo current weather and daily precipitation",
                "GDELT 2.1 document search for city news sentiment",
                "CrisisIQ city socio-economic baseline for non-realtime indicators",
            ],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    async def _weather(self, city: CityBaseline, client: httpx.AsyncClient) -> dict:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={city.latitude}&longitude={city.longitude}"
            "&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m"
            "&daily=precipitation_sum,temperature_2m_max"
            "&forecast_days=1&timezone=auto"
        )
        try:
            response = await client.get(url, timeout=WEATHER_TIMEOUT)
            response.raise_for_status()
            payload = response.json()
        except httpx.HTTPError as exc:
            return {"available": False, "error": str(exc), "temperature_c": None, "rainfall_mm": None, "heatwave_days": 0}

        current = payload.get("current") or {}
        daily = payload.get("daily") or {}
        max_temp = _first(daily.get("temperature_2m_max"), current.get("temperature_2m"))
        rainfall = _first(daily.get("precipitation_sum"), current.get("precipitation"), 0.0)
        heatwave_days = 1 if max_temp is not None and max_temp >= 40 else 0
        rainfall_deviation = _rainfall_deviation(city, rainfall)
        return {
            "available": True,
            "temperature_c": max_temp,
            "humidity_pct": current.get("relative_humidity_2m"),
            "rainfall_mm": rainfall,
            "wind_kph": current.get("wind_speed_10m"),
            "rainfall_deviation": rainfall_deviation,
            "heatwave_days": heatwave_days,
            "provider": "open-meteo",
        }

    async def _news(self, city: CityBaseline, client: httpx.AsyncClient) -> dict:
        query = quote_plus(f'"{city.city}" India (crisis OR crime OR flood OR heatwave OR unemployment OR inflation OR protest)')
        url = (
            "https://api.gdeltproject.org/api/v2/doc/doc"
            f"?query={query}&mode=artlist&format=json&maxrecords=20&sort=hybridrel"
        )
        try:
            response = await client.get(url, timeout=NEWS_TIMEOUT)
            response.raise_for_status()
            articles = (response.json().get("articles") or [])[:20]
        except (httpx.HTTPError, ValueError) as exc:
            fallback = await self._news_rss(city, client)
            if fallback["available"]:
                fallback["fallback_reason"] = str(exc)
                return fallback
            return {"available": False, "error": str(exc), "article_count": 0, "sentiment": 0.0, "headlines": []}

        scored = []
        for article in articles:
            title = article.get("title") or ""
            domain = article.get("domain") or ""
            published = _parse_date(article.get("seendate"))
            score = _headline_sentiment(title)
            scored.append({"title": title, "domain": domain, "published_at": published, "score": score})

        sentiment = round(sum(item["score"] for item in scored) / len(scored), 3) if scored else 0.0
        return {
            "available": True,
            "article_count": len(scored),
            "sentiment": sentiment,
            "headlines": scored[:5],
            "provider": "gdelt",
        }

    async def _news_rss(self, city: CityBaseline, client: httpx.AsyncClient) -> dict:
        query = quote_plus(f'{city.city} India crisis OR crime OR flood OR heatwave OR unemployment OR inflation')
        url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
        try:
            response = await client.get(url, timeout=NEWS_TIMEOUT)
            response.raise_for_status()
            root = ElementTree.fromstring(response.text)
        except (httpx.HTTPError, ElementTree.ParseError) as exc:
            return {"available": False, "error": str(exc), "article_count": 0, "sentiment": 0.0, "headlines": []}

        items = root.findall(".//item")[:20]
        scored = []
        for item in items:
            title = item.findtext("title") or ""
            source = item.findtext("source") or ""
            published = _parse_date(item.findtext("pubDate"))
            score = _headline_sentiment(title)
            scored.append({"title": title, "domain": source, "published_at": published, "score": score})

        sentiment = round(sum(item["score"] for item in scored) / len(scored), 3) if scored else 0.0
        return {
            "available": bool(scored),
            "article_count": len(scored),
            "sentiment": sentiment,
            "headlines": scored[:5],
            "provider": "google-news-rss",
        }

    def _build_features(self, city: CityBaseline, weather: dict, news: dict) -> RiskFeatures:
        rainfall_deviation = float(weather.get("rainfall_deviation") or 0.0)
        heatwave_days = int(weather.get("heatwave_days") or 0)
        news_sentiment = float(news.get("sentiment", 0.0))
        return RiskFeatures(
            region_code=city.code,
            unemployment_rate=city.unemployment_rate,
            inflation_rate=city.inflation_rate,
            crime_rate=city.crime_rate,
            rainfall_deviation=rainfall_deviation,
            heatwave_days=heatwave_days,
            news_sentiment=news_sentiment,
            social_sentiment=news_sentiment * 0.75,
            population_density=city.population_density,
            poverty_rate=city.poverty_rate,
        )


def _first(value, fallback=None, default=None):
    if isinstance(value, list) and value:
        return value[0]
    if value is not None:
        return value
    if fallback is not None:
        return fallback
    return default


def _rainfall_deviation(city: CityBaseline, rainfall_mm: float | None) -> float:
    expected_daily = 3.0
    if city.city in {"Mumbai", "Kolkata", "Guwahati", "Chennai", "Visakhapatnam"}:
        expected_daily = 5.0
    if city.city in {"Jaipur", "Jodhpur", "Kota"}:
        expected_daily = 1.5
    rainfall = float(rainfall_mm or 0.0)
    return round(max(-100.0, min(100.0, ((rainfall - expected_daily) / expected_daily) * 100)), 2)


def _headline_sentiment(title: str) -> float:
    words = {word.strip(".,:;!?()[]{}'\"").lower() for word in title.split()}
    negative = len(words & NEGATIVE_TERMS)
    positive = len(words & POSITIVE_TERMS)
    if negative == positive == 0:
        return 0.0
    return max(-1.0, min(1.0, (positive - negative) / max(positive + negative, 1)))


def _parse_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        if len(value) == 14 and value.isdigit():
            return datetime.strptime(value, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc).isoformat()
        return parsedate_to_datetime(value).isoformat()
    except (TypeError, ValueError):
        return value
