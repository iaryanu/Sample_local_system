import pandas as pd

REQUIRED_COLUMNS = [
    "train_id", "station_from", "station_to",
    "train_type", "time", "compartment", "crowd_base"
]

def load_data(path="traindata.csv"):
    df = pd.read_csv(path)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df


def add_crowd_level(df):
    df = df.copy()

    def get_level(x):
        if x < 0.5:
            return "Low"
        elif x < 0.7:
            return "Medium"
        else:
            return "High"

    df["crowd_level"] = df["crowd_base"].apply(get_level)
    return df


def apply_bias(df):
    df = df.copy()

    df.loc[df["train_type"] == "fast", "crowd_base"] += 0.05

    df.loc[(df["compartment"] >= 4) & (df["compartment"] <= 8), "crowd_base"] += 0.05

    df.loc[(df["time"] >= 8) & (df["time"] <= 10), "crowd_base"] += 0.08
    df.loc[(df["time"] >= 18) & (df["time"] <= 20), "crowd_base"] += 0.08

    df["crowd_base"] = df["crowd_base"].clip(0, 1)

    return df