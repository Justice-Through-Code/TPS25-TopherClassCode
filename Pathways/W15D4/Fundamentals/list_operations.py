# Basic Example 1: Efficient List Operations
# This file demonstrates simple ways to make list operations faster

import time

# Example 1: Using list comprehensions instead of loops
print("=== List Comprehensions vs Regular Loops ===")

# Slower way: using a regular loop
def slow_square_numbers(numbers):
    result = []
    for num in numbers:
        result.append(num ** 2)
    return result

# Faster way: using list comprehension
def fast_square_numbers(numbers):
    return [num ** 2 for num in numbers]

# Test with a list of numbers
test_numbers = list(range(1000))

# Time the slow way
start_time = time.time()
slow_result = slow_square_numbers(test_numbers)
slow_time = time.time() - start_time

# Time the fast way
start_time = time.time()
fast_result = fast_square_numbers(test_numbers)
fast_time = time.time() - start_time

print(f"Slow method took: {slow_time:.4f} seconds")
print(f"Fast method took: {fast_time:.4f} seconds")
print(f"Speed improvement: {slow_time/fast_time:.2f}x faster")

# Example 2: Pre-allocating list size when you know it
print("\n=== Pre-allocating vs Growing Lists ===")

def growing_list(size):
    result = []  # Start with empty list
    for i in range(size):
        result.append(i)
    return result

def preallocated_list(size):
    result = [0] * size  # Pre-allocate the size
    for i in range(size):
        result[i] = i
    return result

size = 10000

# Time growing list
start_time = time.time()
grow_result = growing_list(size)
grow_time = time.time() - start_time

# Time pre-allocated list
start_time = time.time()
prealloc_result = preallocated_list(size)
prealloc_time = time.time() - start_time

print(f"Growing list took: {grow_time:.4f} seconds")
print(f"Pre-allocated list took: {prealloc_time:.4f} seconds")
print(f"Speed improvement: {grow_time/prealloc_time:.2f}x faster")

print("\n🎯 Key Takeaway: Small changes in how you write code can make it faster!")