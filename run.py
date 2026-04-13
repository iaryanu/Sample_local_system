from logic import get_best_option

print(" SmartRail AI (Console Test)")

source = input("Enter Source Station: ")
destination = input("Enter Destination Station: ")
time = int(input("Enter Time (7-12): "))

result = get_best_option(source, destination, time)

if result is None:
    print("\n❌ No trains available for given input")
else:
    print("\n Best Train:", result["train_id"], f"({result['train_type']})")
    print(" Best Compartment:", result["best_compartment"])
    print(" Crowd Level:", result["crowd"])

    print("\nAll Compartments (Least → Most Crowded):")

    for comp in result["full_ranking"]:
        print(f"Coach {comp['compartment']} → {comp['crowd_base']}")