from fastapi.testclient import TestClient

from app.main import app
from app.services.realtime_sources import _headline_sentiment
from app.services.top_cities import TOP_50_CITIES


def _headers(client: TestClient) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": "admin@crisisiq.ai", "password": "CrisisIQ@123"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_top_50_city_registry_has_expected_size() -> None:
    assert len(TOP_50_CITIES) == 50
    assert TOP_50_CITIES[0].code == "IN-MUM"


def test_realtime_cities_route_lists_top_50() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/realtime/cities", headers=_headers(client))
    assert response.status_code == 200
    cities = response.json()
    assert len(cities) == 50
    assert {"code", "city", "state", "latitude", "longitude", "population_millions"} <= set(cities[0])


def test_headline_sentiment_scores_risk_language_negative() -> None:
    assert _headline_sentiment("Flood crisis and crime protest in city") < 0
    assert _headline_sentiment("Investment growth and jobs recovery") > 0
