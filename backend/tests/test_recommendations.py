from app.services.recommendations import build_recommendation


def test_recommendation_contains_actions() -> None:
    rec = build_recommendation("RJ-JAI", "climate", 81.5)
    assert rec.severity_score == 81.5
    assert len(rec.actions) >= 3
    assert "RJ-JAI" in rec.rationale
