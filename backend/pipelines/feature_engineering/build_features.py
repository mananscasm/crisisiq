import pandas as pd

FEATURE_COLUMNS = [
    "unemployment_rate",
    "inflation_rate",
    "crime_rate",
    "rainfall_deviation",
    "heatwave_days",
    "news_sentiment",
    "social_sentiment",
    "population_density",
    "poverty_rate",
]


def build_feature_matrix(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    features = frame[FEATURE_COLUMNS].copy()
    features["sentiment_distress"] = 1 - ((features["news_sentiment"] + features["social_sentiment"] + 2) / 4)
    features["climate_stress"] = features["rainfall_deviation"].abs() / 100 + features["heatwave_days"] / 40
    features["economic_stress"] = features["unemployment_rate"] / 20 + features["inflation_rate"] / 15
    target = frame["crisis_label"].astype(int)
    return features, target
