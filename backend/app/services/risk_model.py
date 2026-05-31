from __future__ import annotations

from pathlib import Path

from app.core.config import get_settings
from app.schemas.api import RiskFeatures

FEATURE_NAMES = [
    "unemployment_rate",
    "inflation_rate",
    "crime_rate",
    "rainfall_deviation",
    "heatwave_days",
    "news_sentiment",
    "social_sentiment",
    "population_density",
    "poverty_rate",
]


class CrisisRiskModel:
    def __init__(self) -> None:
        self.model = None
        self.settings = get_settings()
        path = Path(self.settings.model_path)
        if path.exists():
            try:
                import joblib

                self.model = joblib.load(path)
            except ImportError:
                self.model = None

    def predict(self, features: RiskFeatures) -> tuple[float, float, dict[str, float]]:
        vector = [[float(getattr(features, name)) for name in FEATURE_NAMES]]
        if self.model is not None and hasattr(self.model, "predict_proba"):
            probability = float(self.model.predict_proba(vector)[0][1])
        else:
            probability = self._heuristic_probability(features)

        drivers = self.driver_scores(features)
        risk_score = round(probability * 100, 2)
        return risk_score, round(probability, 4), drivers

    def _heuristic_probability(self, f: RiskFeatures) -> float:
        pressure = (
            0.18 * f.unemployment_rate / 20
            + 0.15 * f.inflation_rate / 15
            + 0.18 * f.crime_rate / 90
            + 0.12 * max(abs(f.rainfall_deviation), 0) / 70
            + 0.10 * f.heatwave_days / 30
            + 0.12 * (1 - ((f.news_sentiment + 1) / 2))
            + 0.10 * (1 - ((f.social_sentiment + 1) / 2))
            + 0.05 * f.poverty_rate / 45
        )
        return max(0.02, min(0.98, float(pressure)))

    def driver_scores(self, f: RiskFeatures) -> dict[str, float]:
        raw = {
            "employment_stress": f.unemployment_rate / 20,
            "price_pressure": f.inflation_rate / 15,
            "public_safety": f.crime_rate / 90,
            "climate_anomaly": (abs(f.rainfall_deviation) / 70 + f.heatwave_days / 30) / 2,
            "sentiment_distress": (2 - f.news_sentiment - f.social_sentiment) / 4,
            "structural_vulnerability": f.poverty_rate / 45,
        }
        return {k: round(max(0.0, min(1.0, float(v))), 3) for k, v in raw.items()}


def classify_category(drivers: dict[str, float]) -> str:
    mapping = {
        "employment_stress": "unemployment",
        "price_pressure": "inflation",
        "public_safety": "crime",
        "climate_anomaly": "climate",
        "sentiment_distress": "sentiment",
        "structural_vulnerability": "poverty",
    }
    return mapping[max(drivers, key=drivers.get)]


def severity_from_score(score: float) -> str:
    if score >= 80:
        return "critical"
    if score >= 60:
        return "high"
    if score >= 35:
        return "moderate"
    return "low"
