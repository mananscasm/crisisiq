from __future__ import annotations

from pathlib import Path

import joblib
import mlflow
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parents[2]
DATASET = ROOT / "datasets" / "demo_crisis_india.csv"
MODEL_DIR = ROOT / "ml" / "models"
REPORT_DIR = ROOT / "ml" / "reports"

import sys

sys.path.append(str(ROOT / "backend"))
from pipelines.cleaning.clean_dataset import clean_crisis_dataset  # noqa: E402
from pipelines.feature_engineering.build_features import build_feature_matrix  # noqa: E402


def evaluate(name: str, estimator: Pipeline, x: pd.DataFrame, y: pd.Series) -> dict[str, float]:
    folds = min(4, y.value_counts().min())
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)
    probabilities = cross_val_predict(estimator, x, y, cv=cv, method="predict_proba")[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "model_name": name,
        "accuracy": accuracy_score(y, predictions),
        "precision": precision_score(y, predictions, zero_division=0),
        "recall": recall_score(y, predictions, zero_division=0),
        "f1": f1_score(y, predictions, zero_division=0),
        "roc_auc": roc_auc_score(y, probabilities),
    }


def main() -> None:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    frame = clean_crisis_dataset(pd.read_csv(DATASET))
    x, y = build_feature_matrix(frame)

    models = {
        "Logistic Regression": Pipeline([("scale", StandardScaler()), ("model", LogisticRegression(max_iter=1000))]),
        "Random Forest": Pipeline([("model", RandomForestClassifier(n_estimators=300, random_state=42, class_weight="balanced"))]),
        "AdaBoost": Pipeline([("model", AdaBoostClassifier(n_estimators=150, random_state=42))]),
        "XGBoost": Pipeline(
            [
                (
                    "model",
                    XGBClassifier(
                        n_estimators=120,
                        max_depth=3,
                        learning_rate=0.08,
                        subsample=0.9,
                        eval_metric="logloss",
                        random_state=42,
                    ),
                )
            ]
        ),
    }

    mlflow.set_tracking_uri(str(ROOT / "mlruns"))
    mlflow.set_experiment("crisisiq-risk-classification")
    results = []
    best_name = ""
    best_score = -1.0
    best_model = None

    for name, estimator in models.items():
        with mlflow.start_run(run_name=name):
            metrics = evaluate(name, estimator, x, y)
            estimator.fit(x, y)
            mlflow.log_metrics({k: v for k, v in metrics.items() if k != "model_name"})
            mlflow.sklearn.log_model(estimator, "model")
            results.append(metrics)
            if metrics["roc_auc"] > best_score:
                best_name = name
                best_score = metrics["roc_auc"]
                best_model = estimator

    assert best_model is not None
    joblib.dump(best_model, MODEL_DIR / "crisis_risk_model.joblib")
    pd.DataFrame(results).sort_values("roc_auc", ascending=False).to_csv(REPORT_DIR / "model_metrics.csv", index=False)
    print(f"best_model={best_name} roc_auc={best_score:.3f}")


if __name__ == "__main__":
    main()
