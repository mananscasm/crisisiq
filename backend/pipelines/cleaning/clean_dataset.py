import pandas as pd

NUMERIC_DEFAULTS = {
    "unemployment_rate": 7.0,
    "inflation_rate": 5.5,
    "crime_rate": 50.0,
    "rainfall_deviation": 0.0,
    "heatwave_days": 0,
    "news_sentiment": 0.0,
    "social_sentiment": 0.0,
    "population_density": 1000.0,
    "poverty_rate": 15.0,
}


def clean_crisis_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    cleaned.columns = [c.strip().lower() for c in cleaned.columns]
    for column, default in NUMERIC_DEFAULTS.items():
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce").fillna(default)
    cleaned["crisis_label"] = pd.to_numeric(cleaned["crisis_label"], errors="coerce").fillna(0).astype(int)
    return cleaned.drop_duplicates(subset=["region_code"]).reset_index(drop=True)
