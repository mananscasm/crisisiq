from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.domain import ModelMetric, PipelineLog, Region, User


REGIONS = [
    ("MH-MUM", "Maharashtra", "Mumbai", 19.076, 72.8777, 12442373),
    ("DL-NDL", "Delhi", "New Delhi", 28.6139, 77.209, 249998),
    ("KA-BLR", "Karnataka", "Bengaluru Urban", 12.9716, 77.5946, 9621551),
    ("WB-KOL", "West Bengal", "Kolkata", 22.5726, 88.3639, 4496694),
    ("RJ-JAI", "Rajasthan", "Jaipur", 26.9124, 75.7873, 3046163),
    ("BR-PAT", "Bihar", "Patna", 25.5941, 85.1376, 2046652),
    ("TN-CHE", "Tamil Nadu", "Chennai", 13.0827, 80.2707, 4646732),
    ("AS-GUW", "Assam", "Kamrup Metropolitan", 26.1445, 91.7362, 1253938),
]


def seed_database(db: Session) -> None:
    if not db.query(User).filter(User.email == "admin@crisisiq.ai").first():
        db.add(
            User(
                email="admin@crisisiq.ai",
                full_name="CrisisIQ Admin",
                role="admin",
                password_hash=hash_password("CrisisIQ@123"),
            )
        )

    for code, state, district, lat, lon, population in REGIONS:
        if not db.query(Region).filter(Region.code == code).first():
            db.add(Region(code=code, state=state, district=district, latitude=lat, longitude=lon, population=population))

    if not db.query(ModelMetric).first():
        db.add_all(
            [
                ModelMetric(model_name="XGBoost", accuracy=0.918, precision=0.902, recall=0.913, f1=0.907, roc_auc=0.954),
                ModelMetric(model_name="Random Forest", accuracy=0.893, precision=0.881, recall=0.874, f1=0.877, roc_auc=0.931),
                ModelMetric(model_name="Logistic Regression", accuracy=0.842, precision=0.821, recall=0.815, f1=0.818, roc_auc=0.887),
            ]
        )

    if not db.query(PipelineLog).first():
        db.add_all(
            [
                PipelineLog(pipeline_name="census_ingestion", status="success", records_processed=742, message="Loaded demographic baseline."),
                PipelineLog(pipeline_name="weather_features", status="success", records_processed=742, message="Computed rainfall and heatwave anomalies."),
                PipelineLog(pipeline_name="sentiment_stream", status="running", records_processed=18320, message="Streaming news and social signals."),
            ]
        )
    db.commit()
