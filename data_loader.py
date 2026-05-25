import pandas as pd


COLUMN_NAMES = [
    "station_id",
    "station_name",
    "pulau",
    "provinsi",
    "kabkota",
    "longitude",
    "latitude",
    "elevasi",
    "curah_hujan",
]


def load_rainfall_data(path: str) -> pd.DataFrame:
    rows = []

    with open(path, encoding="utf-8") as file:
        for line in file:
            parts = [part.strip() for part in line.rstrip("\n").split(",")]
            if len(parts) < len(COLUMN_NAMES):
                continue

            pulau_index = len(parts) - 7
            if pulau_index < 2:
                continue

            rows.append([
                parts[0],
                ", ".join(parts[1:pulau_index]),
                *parts[pulau_index:pulau_index + 7],
            ])

    df = pd.DataFrame(rows, columns=COLUMN_NAMES, dtype=str)

    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["elevasi"] = pd.to_numeric(df["elevasi"], errors="coerce")
    df["curah_hujan"] = pd.to_numeric(df["curah_hujan"], errors="coerce")

    return df.dropna(subset=["longitude", "latitude", "curah_hujan"])
