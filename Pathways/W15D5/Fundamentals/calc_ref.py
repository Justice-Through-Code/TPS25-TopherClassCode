def perform_operation(operation, a, b):
    result = operation(a, b)
    print(f"Result is: {result}")
    return result

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

# Usage
x = 10
y = 5
perform_operation(add, x, y)
perform_operation(subtract, x, y)
perform_operation(multiply, x, y)
perform_operation(divide, x, y)