# Historical Data Filtering and Searching
# This file shows how to filter and search through historical data

# List of historical battles with details
battles = [
    {"name": "Battle of Hastings", "year": 1066, "country": "England", "casualties": 2000},
    {"name": "Battle of Gettysburg", "year": 1863, "country": "USA", "casualties": 51000},
    {"name": "Battle of Waterloo", "year": 1815, "country": "Belgium", "casualties": 65000},
    {"name": "Battle of Stalingrad", "year": 1942, "country": "Russia", "casualties": 2000000},
    {"name": "Battle of Marathon", "year": -490, "country": "Greece", "casualties": 6400}
]

print("All Historical Battles:")
print("-" * 50)
for battle in battles:
    print(f"{battle['name']} ({battle['year']}) - {battle['casualties']:,} casualties")

print("\n" + "=" * 50)

# Filter battles by time period
print("Medieval Battles (500-1500 AD):")
print("-" * 30)
medieval_battles = []
for battle in battles:
    if 500 <= battle['year'] <= 1500:
        medieval_battles.append(battle)

for battle in medieval_battles:
    print(f"• {battle['name']} in {battle['year']}")

print("\n" + "=" * 50)

# Find battles with high casualties
print("Major Battles (over 50,000 casualties):")
print("-" * 40)
major_battles = [b for b in battles if b['casualties'] > 50000]

for battle in major_battles:
    print(f"• {battle['name']}: {battle['casualties']:,} casualties")

print("\n" + "=" * 50)

# Search function
def search_battles_by_country(country_name):
    """Find all battles in a specific country"""
    results = []
    for battle in battles:
        if country_name.lower() in battle['country'].lower():
            results.append(battle)
    return results

# Example search
print("Battles in England:")
print("-" * 20)
english_battles = search_battles_by_country("England")
for battle in english_battles:
    print(f"• {battle['name']} ({battle['year']})")

# Calculate average casualties
total_casualties = sum(battle['casualties'] for battle in battles)
average_casualties = total_casualties / len(battles)
print(f"\nAverage casualties per battle: {average_casualties:,.0f}")