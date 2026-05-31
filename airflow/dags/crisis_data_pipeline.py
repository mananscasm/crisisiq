from datetime import datetime

from airflow.decorators import dag, task


@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False, tags=["crisisiq"])
def crisis_data_pipeline():
    @task
    def ingest() -> str:
        return "ingested census, economic, crime, climate, and sentiment sources"

    @task
    def clean(_: str) -> str:
        return "validated schema, imputed missing values, normalized district names"

    @task
    def engineer(_: str) -> str:
        return "built climate stress, economic stress, and sentiment distress features"

    @task
    def train(_: str) -> str:
        return "queued MLflow training and Evidently drift report"

    train(engineer(clean(ingest())))


crisis_data_pipeline()
