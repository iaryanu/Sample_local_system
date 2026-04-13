import pandas as pd

def load_data(path="traindata.csv"):
    df = pd.read_csv(path)
    return df


def filter_data(df, source, destination, time):

    return df[
        (df["station_from"] == source) &
        (df["station_to"] == destination) &
        (df["time"] == time)
    ]


def add_crowd_level(df):
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

    df["crowd_base"] = df["crowd_base"].clip(0, 1)

    return df