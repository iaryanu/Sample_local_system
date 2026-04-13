import pandas as pd
from data_handling import load_data, apply_bias, add_crowd_level

df = load_data()
df = apply_bias(df)
df = add_crowd_level(df)


STATIONS_ORDER = [
    "Virar", "Nalasopara","Vasai Road" ,"Naigaon",
    "Bhayandar", "Mira Road", "Dahisar", "Borivali",
    "Kandivali", "Malad", "Goregaon", "Jogeshwari",
    "Andheri", "Vile Parle", "Santacruz", "Bandra",
    "Mahim", "Dadar", "Mumbai Central", "Churchgate"
]

def is_before_borivali(station):
    return STATIONS_ORDER.index(station) <= STATIONS_ORDER.index("Borivali")

FAST_STOPS_AFTER_BORIVALI = [
    "Borivali", "Andheri", "Bandra", "Dadar", "Mumbai Central", "Churchgate"
]

def filter_trains(source, destination, time):
    filtered = df[
        (df["station_from"] == source) &
        (df["station_to"] == destination) &
        (df["time"] == time)
    ]

    valid_trains = []

    for train_id in filtered["train_id"].unique():
        train_data = filtered[filtered["train_id"] == train_id]
        train_type = train_data.iloc[0]["train_type"]

        if train_type == "fast":
            if not is_before_borivali(source):
                if source not in FAST_STOPS_AFTER_BORIVALI:
                    continue

        valid_trains.append(train_data)

    return valid_trains


def select_best_train(valid_trains):
     best_train = None
     best_score = float("inf")

     for train in valid_trains:
        avg_crowd = train["crowd_base"].mean()

        if avg_crowd < best_score:
            best_score = avg_crowd
            best_train = train

     return best_train


def rank_compartments(train):
    return train.sort_values(by="crowd_base")


def get_best_option(source, destination, time):
    valid_trains = filter_trains(source, destination, time)

    if not valid_trains:
        return None

    best_train = select_best_train(valid_trains)
    ranked = rank_compartments(best_train)

    best_compartment = ranked.iloc[0]

    return {
        "train_id": best_train.iloc[0]["train_id"],
        "train_type": best_train.iloc[0]["train_type"],
        "best_compartment": int(best_compartment["compartment"]),
        "crowd": float(best_compartment["crowd_base"]),
        "full_ranking": ranked[["compartment", "crowd_base"]].to_dict(orient="records")
    }