students = [
    {"name": "Alice", "math": 85, "english": 92, "science": 78},
    {"name": "Bob", "math": 90, "english": 88, "science": 95},
    {"name": "Charlie", "math": 76, "english": 84, "science": 89}
]

def calculate_average(student):
    total = student["math"] + student["english"] + student["science"]
    avg = total / 3
    print(f"{student['name']}'s average: {avg}")
    return avg

for student in students:
    calculate_average(student)