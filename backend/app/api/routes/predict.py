from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.models.domain import Alert, Prediction, Recommendation, Region, User
from app.schemas.api import PredictionOut, RiskFeatures
from app.services.recommendations import build_recommendation
from app.services.risk_model import CrisisRiskModel, classify_category, severity_from_score

router = APIRouter(prefix="/predict", tags=["prediction"])
model = CrisisRiskModel()


@router.post("", response_model=PredictionOut)
def predict(payload: RiskFeatures, db: Session = Depends(get_db), _: User = Depends(current_user)) -> PredictionOut:
    region = db.query(Region).filter(Region.code == payload.region_code).first()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    risk_score, probability, drivers = model.predict(payload)
    category = classify_category(drivers)
    severity = severity_from_score(risk_score)
    prediction = Prediction(
        region_id=region.id,
        risk_score=risk_score,
        probability=probability,
        crisis_category=category,
        severity=severity,
        drivers=drivers,
    )
    db.add(prediction)

    recommendation = build_recommendation(region.code, category, risk_score)
    db.add(
        Recommendation(
            region_id=region.id,
            category=category,
            severity_score=risk_score,
            actions=recommendation.actions,
            rationale=recommendation.rationale,
        )
    )

    if risk_score >= 60:
        db.add(
            Alert(
                region_id=region.id,
                title=f"{severity.title()} crisis risk in {region.district}",
                message=f"{category.title()} driver pushed CrisisIQ risk to {risk_score}.",
                severity=severity,
            )
        )
    db.commit()
    db.refresh(prediction)
    return PredictionOut(
        id=prediction.id,
        region_code=region.code,
        risk_score=risk_score,
        probability=probability,
        crisis_category=category,
        severity=severity,
        drivers=drivers,
        created_at=prediction.created_at,
    )
