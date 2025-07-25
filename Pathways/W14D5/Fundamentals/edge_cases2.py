def divide_numbers(a, b):
    if b == 0:  # Edge case: division by zero
        return "Cannot divide by zero!"
    return a / b

# Normal case
print(divide_numbers(10, 2))  # Output: 5.0

# Edge case
print(divide_numbers(10, 0))  # Output: Cannot divide by zero!