# Basic Error Handling for Beginners
# This file shows how to catch and handle common errors

print("=== Basic Error Handling Examples ===\n")

# Example 1: Handling division by zero
print("1. Division by Zero Protection:")
try:
    number = 10
    divisor = 0
    result = number / divisor
    print(f"Result: {result}")
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
    print("Using default value of 0 instead.")
    result = 0

print(f"Final result: {result}\n")

# Example 2: Handling invalid input types
print("2. Type Error Protection:")
try:
    text = "hello"
    number = 5
    result = text + number  # This will cause a TypeError
except TypeError:
    print("Error: Cannot add text and number!")
    print("Converting number to text instead.")
    result = text + str(number)

print(f"Final result: {result}\n")

# Example 3: Handling file operations
print("3. File Not Found Protection:")
try:
    with open("nonexistent_file.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("Error: File not found!")
    print("Creating a default message instead.")
    content = "Default content - file was missing"

print(f"Content: {content}\n")

# Example 4: Multiple error types
print("4. Multiple Error Types:")
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    except TypeError:
        print("Both inputs must be numbers!")
        return None

# Test the function
print(f"safe_divide(10, 2) = {safe_divide(10, 2)}")
print(f"safe_divide(10, 0) = {safe_divide(10, 0)}")
print(f"safe_divide(10, 'hello') = {safe_divide(10, 'hello')}")