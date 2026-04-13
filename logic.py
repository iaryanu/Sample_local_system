import pandas as pd
from data_handling import load_data, apply_bias, add_crowd_level

df = load_data()
df = apply_bias(df)
df = add_crowd_level(df)

STATIONS_ORDER = [
    "Virar", "Nalasopara", "Vasai Road", "Naigaon",
    "Bhayandar", "Mira Road", "Dahisar", "Borivali",
    "Kandivali", "Malad", "Goregaon", "Jogeshwari",
    "Andheri", "Vile Parle", "Santacruz", "Bandra",
    "Mahim", "Dadar", "Mumbai Central", "Churchgate"
]

FAST_STOPS_AFTER_BORIVALI = [
    "Borivali", "Andheri", "Bandra", "Dadar", "Mumbai Central", "Churchgate"
]


def filter_trains(source, destination, time):
    source_idx = STATIONS_ORDER.index(source)
    dest_idx = STATIONS_ORDER.index(destination)

    filtered = df[(df["time"] >= time - 1) & (df["time"] <= time + 1)]

    valid_trains = []

    for train_id, train_data in filtered.groupby("train_id"):

        train_start = train_data.iloc[0]["station_from"]
        train_end = train_data.iloc[0]["station_to"]
        train_type = train_data.iloc[0]["train_type"]

        start_idx = STATIONS_ORDER.index(train_start)
        end_idx = STATIONS_ORDER.index(train_end)

        if not (source_idx >= start_idx and dest_idx <= end_idx):
            continue

        if train_type == "fast":
            if source not in FAST_STOPS_AFTER_BORIVALI or destination not in FAST_STOPS_AFTER_BORIVALI:
                continue

        valid_trains.append(train_data)

    return valid_trains


def compute_score(train, source, destination):
    avg_crowd = train["crowd_base"].mean()

    source_idx = STATIONS_ORDER.index(source)
    dest_idx = STATIONS_ORDER.index(destination)

    distance = abs(dest_idx - source_idx)

    score = avg_crowd + (distance * 0.04)

    return score


def rank_trains(valid_trains, source, destination):
    scored_trains = []

    for train in valid_trains:
        score = compute_score(train, source, destination)

        scored_trains.append((train, score))

    scored_trains.sort(key=lambda x: x[1])

    return scored_trains[:3]  


def rank_compartments(train):
    return train.sort_values(by="crowd_base")


def get_best_options(source, destination, time):
    valid_trains = filter_trains(source, destination, time)

    if not valid_trains:
        return None

    top_trains = rank_trains(valid_trains, source, destination)

    results = []

    for train, score in top_trains:
        ranked = rank_compartments(train)
        best_compartment = ranked.iloc[0]

        results.append({
            "train_id": train.iloc[0]["train_id"],
            "train_type": train.iloc[0]["train_type"],
            "score": round(score, 3),
            "best_compartment": int(best_compartment["compartment"]),
            "crowd": float(best_compartment["crowd_base"]),
            "full_ranking": ranked[["compartment", "crowd_base"]].to_dict(orient="records")
        })

    return results