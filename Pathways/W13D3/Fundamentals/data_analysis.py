# Basic Historical Data Analysis
# This file demonstrates simple analysis techniques on historical data

# Roman Emperor data with reign lengths
roman_emperors = [
    {"name": "Augustus", "start_year": -27, "end_year": 14, "dynasty": "Julio-Claudian"},
    {"name": "Tiberius", "start_year": 14, "end_year": 37, "dynasty": "Julio-Claudian"},
    {"name": "Caligula", "start_year": 37, "end_year": 41, "dynasty": "Julio-Claudian"},
    {"name": "Claudius", "start_year": 41, "end_year": 54, "dynasty": "Julio-Claudian"},
    {"name": "Nero", "start_year": 54, "end_year": 68, "dynasty": "Julio-Claudian"},
    {"name": "Vespasian", "start_year": 69, "end_year": 79, "dynasty": "Flavian"},
    {"name": "Titus", "start_year": 79, "end_year": 81, "dynasty": "Flavian"},
    {"name": "Domitian", "start_year": 81, "end_year": 96, "dynasty": "Flavian"},
    {"name": "Trajan", "start_year": 98, "end_year": 117, "dynasty": "Nerva-Antonine"},
    {"name": "Hadrian", "start_year": 117, "end_year": 138, "dynasty": "Nerva-Antonine"}
]

print("Roman Emperor Reign Analysis")
print("=" * 40)

# Calculate reign lengths
print("Reign Lengths:")
print("-" * 20)
reign_lengths = []
for emperor in roman_emperors:
    length = emperor['end_year'] - emperor['start_year']
    reign_lengths.append(length)
    print(f"{emperor['name']}: {length} years")

print(f"\nStatistics:")
print("-" * 15)
print(f"Average reign: {sum(reign_lengths) / len(reign_lengths):.1f} years")
print(f"Shortest reign: {min(reign_lengths)} years")
print(f"Longest reign: {max(reign_lengths)} years")

# Find the emperor with longest reign
longest_index = reign_lengths.index(max(reign_lengths))
longest_emperor = roman_emperors[longest_index]
print(f"Longest reigning emperor: {longest_emperor['name']}")

print("\n" + "=" * 40)

# Analyze by dynasty
print("Dynasty Analysis:")
print("-" * 20)

# Count emperors per dynasty
dynasty_counts = {}
dynasty_years = {}

for emperor in roman_emperors:
    dynasty = emperor['dynasty']
    reign_length = emperor['end_year'] - emperor['start_year']
    
    # Count emperors
    if dynasty in dynasty_counts:
        dynasty_counts[dynasty] += 1
        dynasty_years[dynasty] += reign_length
    else:
        dynasty_counts[dynasty] = 1
        dynasty_years[dynasty] = reign_length

print("Emperors per dynasty:")
for dynasty, count in dynasty_counts.items():
    avg_reign = dynasty_years[dynasty] / count
    print(f"• {dynasty}: {count} emperors, avg reign {avg_reign:.1f} years")

print("\n" + "=" * 40)

# Timeline analysis
print("Century Analysis:")
print("-" * 20)

first_century = [emp for emp in roman_emperors if emp['start_year'] >= 1 and emp['start_year'] <= 100]
second_century = [emp for emp in roman_emperors if emp['start_year'] >= 101 and emp['start_year'] <= 200]

print(f"1st century emperors: {len(first_century)}")
for emp in first_century:
    print(f"  • {emp['name']} ({emp['start_year']}-{emp['end_year']})")

print(f"\n2nd century emperors: {len(second_century)}")
for emp in second_century:
    print(f"  • {emp['name']} ({emp['start_year']}-{emp['end_year']})")

# Simple trend analysis
early_avg = sum(emp['end_year'] - emp['start_year'] for emp in first_century) / len(first_century) if first_century else 0
late_avg = sum(emp['end_year'] - emp['start_year'] for emp in second_century) / len(second_century) if second_century else 0

print(f"\nAverage reign length:")
print(f"1st century: {early_avg:.1f} years")
print(f"2nd century: {late_avg:.1f} years")