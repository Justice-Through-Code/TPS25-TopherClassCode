# Basic Example 2: Efficient String Operations
# This file shows how to work with strings more efficiently

import time

# Example 1: String concatenation - join() vs += operator
print("=== String Concatenation Methods ===")

words = ["apple", "banana", "cherry", "date", "elderberry"] * 200  # 1000 words

# Slower way: using += to build strings
def slow_string_join(word_list):
    result = ""
    for word in word_list:
        result += word + " "
    return result.strip()

# Faster way: using join()
def fast_string_join(word_list):
    return " ".join(word_list)

# Time the slow way
start_time = time.time()
slow_result = slow_string_join(words)
slow_time = time.time() - start_time

# Time the fast way
start_time = time.time()
fast_result = fast_string_join(words)
fast_time = time.time() - start_time

print(f"Using += took: {slow_time:.4f} seconds")
print(f"Using join() took: {fast_time:.4f} seconds")
print(f"Speed improvement: {slow_time/fast_time:.2f}x faster")

# Example 2: String formatting methods
print("\n=== String Formatting Methods ===")

name = "Alice"
age = 25
city = "New York"

# Different ways to format strings (from slowest to fastest)
def old_formatting():
    return "Hello, my name is %s, I'm %d years old, and I live in %s." % (name, age, city)

def format_method():
    return "Hello, my name is {}, I'm {} years old, and I live in {}.".format(name, age, city)

def f_string_formatting():
    return f"Hello, my name is {name}, I'm {age} years old, and I live in {city}."

# Time each method (run many times to see the difference)
iterations = 100000

methods = [
    ("Old % formatting", old_formatting),
    (".format() method", format_method),
    ("f-string formatting", f_string_formatting)
]

for method_name, method_func in methods:
    start_time = time.time()
    for _ in range(iterations):
        result = method_func()
    end_time = time.time() - start_time
    print(f"{method_name}: {end_time:.4f} seconds")

print("\n=== String Search Optimization ===")

# Example 3: Checking if string starts with something
text = "Hello, this is a sample text for testing purposes."

# Multiple ways to check if string starts with "Hello"
def using_slice():
    return text[:5] == "Hello"

def using_startswith():
    return text.startswith("Hello")

# startswith() is more readable and often faster
print(f"Using slice [0:5]: {using_slice()}")
print(f"Using startswith(): {using_startswith()}")

print("\n🎯 Key Takeaway: Choose the right string method for better performance!")