from fastapi.testclient import TestClient
import pytest

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def auth_header(client: TestClient) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"email": "admin@crisisiq.ai", "password": "CrisisIQ@123"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_health(client: TestClient) -> None:
    assert client.get("/health").json()["status"] == "ok"


def test_prediction_creates_risk_score(client: TestClient) -> None:
    payload = {
        "region_code": "BR-PAT",
        "unemployment_rate": 12.6,
        "inflation_rate": 7.9,
        "crime_rate": 76,
        "rainfall_deviation": -28,
        "heatwave_days": 16,
        "news_sentiment": -0.41,
        "social_sentiment": -0.46,
        "population_density": 1823,
        "poverty_rate": 28
    }
    response = client.post("/api/v1/predict", json=payload, headers=auth_header(client))
    assert response.status_code == 200
    body = response.json()
    assert body["risk_score"] > 50
    assert body["crisis_category"] in {"unemployment", "inflation", "crime", "climate", "sentiment", "poverty"}
