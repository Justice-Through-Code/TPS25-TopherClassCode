# File 1: Basic Try-Except
# Understanding the fundamentals of error handling

print("=== Basic Try-Except Examples ===\n")

# Example 1: Division by zero
print("Example 1: Preventing division by zero")
try:
    number = 10
    result = number / 0  # This will cause an error
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")

print()

# Example 2: Converting string to integer
print("Example 2: Converting invalid input to integer")
try:
    user_input = "hello"  # This cannot be converted to int
    number = int(user_input)
    print(f"Number: {number}")
except ValueError:
    print("Error: Invalid input - cannot convert to integer!")

print()

# Example 3: Accessing list index that doesn't exist
print("Example 3: Accessing invalid list index")
try:
    my_list = [1, 2, 3]
    print(f"Item at index 5: {my_list[5]}")  # Index 5 doesn't exist
except IndexError:
    print("Error: List index out of range!")

print()

# Example 4: Without try-except vs with try-except
print("Example 4: Program continues after handling error")
print("Processing items...")

items = [1, 2, "three", 4]
for item in items:
    try:
        doubled = item * 2
        print(f"{item} * 2 = {doubled}")
    except TypeError:
        print(f"Cannot multiply {item} by 2 - skipping")

print("Program finished successfully!")