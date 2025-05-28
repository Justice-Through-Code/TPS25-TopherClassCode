# File 2: Multiple Exception Types
# Handling different types of errors with specific responses

print("=== Handling Multiple Exception Types ===\n")

# Example 1: Multiple except blocks
print("Example 1: Calculator with multiple error types")
def safe_calculator(a, b, operation):
    try:
        if operation == "divide":
            result = a / b
        elif operation == "add":
            result = a + b
        elif operation == "multiply":
            result = a * b
        else:
            result = "Unknown operation"
        
        return result
    
    except ZeroDivisionError:
        return "Error: Cannot divide by zero!"
    except TypeError:
        return "Error: Invalid data types for calculation!"

# Test the calculator
print(safe_calculator(10, 2, "divide"))    # Normal case
print(safe_calculator(10, 0, "divide"))    # Division by zero
print(safe_calculator("10", 2, "add"))     # Type error

print()

# Example 2: Catching multiple exceptions in one block
print("Example 2: Multiple exceptions in one except block")
def process_user_data(data_list, index):
    try:
        # Convert to integer and access list
        value = int(data_list[index])
        return f"Value at index {index}: {value}"
    
    except (ValueError, IndexError, TypeError) as error:
        return f"Error processing data: {type(error).__name__}"

# Test with different error scenarios
test_data = ["1", "2", "hello", "4"]
print(process_user_data(test_data, 2))  # ValueError (can't convert "hello")
print(process_user_data(test_data, 10)) # IndexError (index doesn't exist)
print(process_user_data(None, 0))       # TypeError (None is not subscriptable)

print()

# Example 3: Generic exception handling
print("Example 3: Catching any exception with Exception")
def risky_operation(x):
    try:
        # Various operations that might fail
        result = int(x) / len(x)
        return result
    except ZeroDivisionError:
        return "Specific error: Division by zero"
    except ValueError:
        return "Specific error: Cannot convert to integer"
    except Exception as e:
        return f"Unexpected error: {e}"

# Test different scenarios
print(risky_operation("123"))  # TypeError (int has no len)
print(risky_operation("0"))    # ZeroDivisionError  
print(risky_operation("abc"))  # ValueError