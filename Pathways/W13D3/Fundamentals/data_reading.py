# Basic Historical Data Reading
# This file demonstrates how to read and display historical data

# Simple list of historical events with years
historical_events = [
    ("Fall of Roman Empire", 476),
    ("Norman Conquest of England", 1066),
    ("Black Death begins", 1347),
    ("Columbus reaches Americas", 1492),
    ("French Revolution begins", 1789)
]

print("Historical Events:")
print("-" * 30)

# Loop through and display each event
for event, year in historical_events:
    print(f"{year}: {event}")

print("\n" + "=" * 40)

# Working with a simple dictionary of population data
ancient_cities = {
    "Rome": 450000,
    "Alexandria": 400000,
    "Antioch": 200000,
    "Athens": 100000,
    "Sparta": 35000
}

print("Ancient City Populations (estimated):")
print("-" * 35)

# Display city populations
for city, population in ancient_cities.items():
    print(f"{city}: {population:,} people")

# Find the largest city
largest_city = max(ancient_cities, key=ancient_cities.get)
print(f"\nLargest city: {largest_city} with {ancient_cities[largest_city]:,} people")