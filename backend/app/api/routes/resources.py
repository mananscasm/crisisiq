from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.api.deps import current_user
from app.db.session import get_db
from app.models.domain import Alert, PipelineLog, Recommendation, Region, User
from app.schemas.api import AlertOut, RegionOut

router = APIRouter(tags=["resources"])


@router.get("/regions", response_model=list[RegionOut])
def regions(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[Region]:
    return db.query(Region).order_by(Region.state, Region.district).all()


@router.get("/alerts", response_model=list[AlertOut])
def alerts(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[Alert]:
    return db.query(Alert).order_by(desc(Alert.created_at)).limit(100).all()


@router.get("/recommendations")
def recommendations(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[dict]:
    rows = db.query(Recommendation).order_by(desc(Recommendation.created_at)).limit(100).all()
    return [
        {
            "region_code": r.region.code,
            "district": r.region.district,
            "category": r.category,
            "severity_score": r.severity_score,
            "actions": r.actions,
            "rationale": r.rationale,
            "created_at": r.created_at,
        }
        for r in rows
    ]


@router.get("/pipelines")
def pipelines(db: Session = Depends(get_db), _: User = Depends(current_user)) -> list[dict]:
    logs = db.query(PipelineLog).order_by(desc(PipelineLog.created_at)).limit(100).all()
    return [
        {
            "pipeline_name": log.pipeline_name,
            "status": log.status,
            "records_processed": log.records_processed,
            "message": log.message,
            "created_at": log.created_at,
        }
        for log in logs
    ]


@router.post("/train")
def train(_: User = Depends(current_user)) -> dict:
    return {
        "status": "queued",
        "message": "Training job accepted. In Docker, run `python ml/training/train_models.py` or trigger the Airflow DAG.",
    }
