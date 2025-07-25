def perform_operation(operation, a, b):
    result = operation(a, b)
    print(f"Result is: {result}")
    return result

def add(a, b):
    result = a + b
    return result

def subtract(a, b):
    result = a - b
    print(f"Results are: {result}")
    return result

def multiply(a, b):
    result = a * b
    print("Multiplying " + str(a) + " and " + str(b))
    print("Result is: " + str(result))
    return result

def divide(a, b):
    result = a / b
    print("Dividing " + str(a) + " by " + str(b))
    print("Result is: " + str(result))
    return result

# Usage
x = 10
y = 5
add(x, y)
subtract(x, y)
multiply(x, y)
divide(x, y)