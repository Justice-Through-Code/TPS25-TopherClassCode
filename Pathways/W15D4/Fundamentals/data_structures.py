# Basic Example 3: Choosing the Right Data Structure
# This file shows how picking the right data structure can improve performance

import time

# Example 1: Finding items - List vs Set
print("=== Finding Items: List vs Set ===")

# Create test data
items_list = list(range(10000))  # List with 10,000 numbers
items_set = set(range(10000))    # Set with same 10,000 numbers

target = 9999  # Look for this number (worst case - it's at the end)

# Search in list (slow)
start_time = time.time()
found_in_list = target in items_list
list_time = time.time() - start_time

# Search in set (fast)
start_time = time.time()
found_in_set = target in items_set
set_time = time.time() - start_time

print(f"Found in list: {found_in_list} (took {list_time:.6f} seconds)")
print(f"Found in set: {found_in_set} (took {set_time:.6f} seconds)")
print(f"Set is {list_time/set_time:.0f}x faster for searching!")

# Example 2: Counting items - Dictionary vs List
print("\n=== Counting Items: Dictionary vs Manual Counting ===")

words = ["apple", "banana", "apple", "cherry", "banana", "apple"] * 1000

# Slow way: count manually each time
def slow_count_words(word_list):
    unique_words = list(set(word_list))  # Get unique words
    counts = {}
    for word in unique_words:
        counts[word] = word_list.count(word)  # This is slow!
    return counts

# Fast way: count as we go
def fast_count_words(word_list):
    counts = {}
    for word in word_list:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

# Even faster way: using get() method
def fastest_count_words(word_list):
    counts = {}
    for word in word_list:
        counts[word] = counts.get(word, 0) + 1
    return counts

# Time each method
start_time = time.time()
slow_result = slow_count_words(words)
slow_time = time.time() - start_time

start_time = time.time()
fast_result = fast_count_words(words)
fast_time = time.time() - start_time

start_time = time.time()
fastest_result = fastest_count_words(words)
fastest_time = time.time() - start_time

print(f"Slow counting: {slow_time:.4f} seconds")
print(f"Fast counting: {fast_time:.4f} seconds")
print(f"Fastest counting: {fastest_time:.4f} seconds")

# Example 3: Removing duplicates
print("\n=== Removing Duplicates: Different Approaches ===")

numbers_with_duplicates = [1, 2, 3, 2, 4, 1, 5, 3, 6, 4] * 500

# Method 1: Using a loop (slow)
def slow_remove_duplicates(items):
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result

# Method 2: Using set (fast, but loses order)
def fast_remove_duplicates(items):
    return list(set(items))

# Method 3: Using set but keeping order (fastest of ordered methods)
def ordered_remove_duplicates(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Time each method
start_time = time.time()
slow_unique = slow_remove_duplicates(numbers_with_duplicates)
slow_time = time.time() - start_time

start_time = time.time()
fast_unique = fast_remove_duplicates(numbers_with_duplicates)
fast_time = time.time() - start_time

start_time = time.time()
ordered_unique = ordered_remove_duplicates(numbers_with_duplicates)
ordered_time = time.time() - start_time

print(f"Slow method (with order): {slow_time:.4f} seconds")
print(f"Fast method (no order): {fast_time:.4f} seconds")
print(f"Ordered method: {ordered_time:.4f} seconds")

print("\n🎯 Key Takeaway: The right data structure makes a huge difference!")