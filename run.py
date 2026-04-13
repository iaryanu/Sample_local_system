from logic import get_best_options, STATIONS_ORDER

print(" SmartRail AI (Console Test)\n")


print("Available Stations:")
print(", ".join(STATIONS_ORDER))


def normalize_station(name):
    return name.strip().title()


source = normalize_station(input("\nEnter Source Station: "))
destination = normalize_station(input("Enter Destination Station: "))

if source not in STATIONS_ORDER or destination not in STATIONS_ORDER:
    print("\n Invalid station entered.")
    exit()

if source == destination:
    print("\n Source and destination cannot be same.")
    exit()

try:
    time = int(input("Enter Time (0–23): "))
    if time < 0 or time > 23:
        raise ValueError
except ValueError:
    print("\n Invalid time.")
    exit()


results = get_best_options(source, destination, time)

if results is None:
    print("\n No trains available for given input")
else:
    print("\n Top 3 Train Recommendations:\n")

    for i, result in enumerate(results, start=1):
        print(f"🔹 Option {i}")
        print(f"Train: {result['train_id']} ({result['train_type']})")
        print(f"Best Compartment: {result['best_compartment']}")

        crowd = result["crowd"]
        if crowd < 0.5:
            level = "Low"
        elif crowd < 0.7:
            level = "Medium"
        else:
            level = "High"

        print(f"Crowd: {level} ({round(crowd, 2)})")
        print(f"Score: {result['score']}")

        print("Compartments (Least → Most Crowded):")
        for comp in result["full_ranking"]:
            c = comp["crowd_base"]

            if c < 0.5:
                lvl = "Low"
            elif c < 0.7:
                lvl = "Medium"
            else:
                lvl = "High"

            print(f"  Coach {comp['compartment']} → {lvl} ({round(c, 2)})")

        print("-" * 40)