# Basic Refactoring Example 3: Removing Code Duplication
# This shows how to eliminate repeated code using functions

print("=== BEFORE REFACTORING ===")
print("Code with lots of repetition:")

# Bad code - same logic repeated multiple times
print("Student 1:")
name1 = "John"
math_grade1 = 85
english_grade1 = 92
average1 = (math_grade1 + english_grade1) / 2
print(f"Name: {name1}")
print(f"Math: {math_grade1}, English: {english_grade1}")
print(f"Average: {average1}")
if average1 >= 90:
    print("Grade: A")
elif average1 >= 80:
    print("Grade: B")
else:
    print("Grade: C")

print("\nStudent 2:")
name2 = "Sarah"
math_grade2 = 78
english_grade2 = 84
average2 = (math_grade2 + english_grade2) / 2
print(f"Name: {name2}")
print(f"Math: {math_grade2}, English: {english_grade2}")
print(f"Average: {average2}")
if average2 >= 90:
    print("Grade: A")
elif average2 >= 80:
    print("Grade: B")
else:
    print("Grade: C")

print("\n=== AFTER REFACTORING ===")
print("Clean code without repetition:")

# Good code - logic written once, used multiple times
def calculate_average(math_score, english_score):
    """Calculate average of two scores"""
    return (math_score + english_score) / 2

def get_letter_grade(average):
    """Convert numerical average to letter grade"""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    else:
        return "C"

def display_student_report(name, math_score, english_score):
    """Display complete student grade report"""
    print(f"Name: {name}")
    print(f"Math: {math_score}, English: {english_score}")
    
    average = calculate_average(math_score, english_score)
    print(f"Average: {average}")
    
    letter_grade = get_letter_grade(average)
    print(f"Grade: {letter_grade}")

# Using the refactored functions
print("Student 1:")
display_student_report("John", 85, 92)

print("\nStudent 2:")
display_student_report("Sarah", 78, 84)

print("\nStudent 3:")  # Easy to add more students now!
display_student_report("Mike", 94, 88)

print("\n=== WHY THIS IS BETTER ===")
print("✓ No repeated code - follow the DRY principle (Don't Repeat Yourself)")
print("✓ Changes only need to be made in one place")
print("✓ Less chance of making mistakes")
print("✓ Much easier to add new students")