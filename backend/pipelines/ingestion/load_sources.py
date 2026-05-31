from pathlib import Path

import pandas as pd


def load_demo_dataset(path: str | Path = "datasets/demo_crisis_india.csv") -> pd.DataFrame:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    return pd.read_csv(dataset_path)


def ingest_all_sources() -> pd.DataFrame:
    # Production connectors can be added here for MOSPI, NCRB, IMD, census, news, and social APIs.
    return load_demo_dataset()


if __name__ == "__main__":
    frame = ingest_all_sources()
    print(f"ingested_rows={len(frame)}")
