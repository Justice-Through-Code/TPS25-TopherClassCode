# Basic Refactoring Example 1: Extracting Functions
# This shows how to take messy code and make it cleaner

print("=== BEFORE REFACTORING ===")
print("Messy code that does everything in one place:")

# Bad code - everything mixed together
name = "Alice"
age = 25
city = "New York"
print("Name: " + name)
print("Age: " + str(age))
print("City: " + city)
if age >= 18:
    print("Status: Adult")
else:
    print("Status: Minor")

print("\n=== AFTER REFACTORING ===")
print("Clean code with separate functions:")

# Good code - organized into functions
def display_person_info(name, age, city):
    """Display a person's basic information"""
    print("Name: " + name)
    print("Age: " + str(age))
    print("City: " + city)

def get_age_status(age):
    """Determine if person is adult or minor"""
    if age >= 18:
        return "Adult"
    else:
        return "Minor"

def display_complete_profile(name, age, city):
    """Display complete person profile"""
    display_person_info(name, age, city)
    status = get_age_status(age)
    print("Status: " + status)

# Using the refactored functions
display_complete_profile("Alice", 25, "New York")

print("\n=== WHY THIS IS BETTER ===")
print("✓ Each function has one clear job")
print("✓ Code is easier to read and understand")
print("✓ Functions can be reused")
print("✓ Easier to test individual parts")