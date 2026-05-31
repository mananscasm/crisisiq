from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.models.domain import ModelMetric, Prediction, Region, User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview")
def overview(db: Session = Depends(get_db), _: User = Depends(current_user)) -> dict:
    predictions = db.query(Prediction).order_by(desc(Prediction.created_at)).limit(50).all()
    regions = db.query(Region).all()
    avg_risk = round(sum(p.risk_score for p in predictions) / len(predictions), 2) if predictions else 0
    return {
        "regions_monitored": len(regions),
        "average_risk": avg_risk,
        "critical_alerts": sum(1 for p in predictions if p.severity == "critical"),
        "sentiment_index": -0.18,
        "top_regions": [
            {
                "region": p.region.code,
                "district": p.region.district,
                "state": p.region.state,
                "risk_score": p.risk_score,
                "severity": p.severity,
                "category": p.crisis_category,
                "lat": p.region.latitude,
                "lng": p.region.longitude,
            }
            for p in predictions[:10]
        ],
    }


@router.get("/model-comparison")
def model_comparison(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[dict]:
    metrics = db.query(ModelMetric).order_by(desc(ModelMetric.roc_auc)).all()
    return [
        {
            "model_name": m.model_name,
            "accuracy": m.accuracy,
            "precision": m.precision,
            "recall": m.recall,
            "f1": m.f1,
            "roc_auc": m.roc_auc,
            "created_at": m.created_at,
        }
        for m in metrics
    ]


@router.get("/forecast")
def forecast(_: User = Depends(current_user)) -> list[dict]:
    return [
        {"month": "Jan", "risk": 42, "forecast": 45},
        {"month": "Feb", "risk": 46, "forecast": 49},
        {"month": "Mar", "risk": 51, "forecast": 53},
        {"month": "Apr", "risk": 58, "forecast": 61},
        {"month": "May", "risk": 63, "forecast": 66},
        {"month": "Jun", "risk": 67, "forecast": 70},
    ]
