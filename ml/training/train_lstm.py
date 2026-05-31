from pathlib import Path

import numpy as np


def build_demo_lstm_series() -> tuple[np.ndarray, np.ndarray]:
    timeline = np.linspace(0, 12, 120)
    risk = 45 + 12 * np.sin(timeline) + 0.8 * timeline
    x, y = [], []
    for idx in range(12, len(risk)):
        x.append(risk[idx - 12 : idx])
        y.append(risk[idx])
    return np.array(x)[..., None], np.array(y)


def main() -> None:
    from tensorflow import keras

    x, y = build_demo_lstm_series()
    model = keras.Sequential(
        [
            keras.layers.Input(shape=(12, 1)),
            keras.layers.LSTM(32),
            keras.layers.Dense(16, activation="relu"),
            keras.layers.Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    model.fit(x, y, epochs=10, batch_size=8, verbose=1)
    output = Path(__file__).resolve().parents[1] / "models" / "lstm_forecaster.keras"
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(output)


if __name__ == "__main__":
    main()
