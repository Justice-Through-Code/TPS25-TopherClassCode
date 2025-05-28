# Edge Cases in ML - Basic Examples
# This file shows how to handle common edge cases in data and ML

print("=== Handling Edge Cases - Basics ===\n")

# Example 1: Empty data handling
print("1. Empty Data Edge Cases:")
def handle_empty_data(data):
    """Handle the edge case of empty data"""
    if not data:  # Empty list, None, etc.
        print("Warning: No data provided!")
        return "No data to process"
    
    if len(data) == 0:
        print("Warning: Empty dataset!")
        return "Empty dataset"
    
    return f"Processing {len(data)} items"

# Test with different empty cases
test_cases = [[], None, [[1, 2], [3, 4]], ""]
for i, case in enumerate(test_cases):
    print(f"Test {i+1}: {handle_empty_data(case)}")
print()

# Example 2: Invalid values in data
print("2. Invalid Values Edge Cases:")
def clean_data(data_list):
    """Remove invalid values from data"""
    if not data_list:
        return []
    
    cleaned = []
    invalid_count = 0
    
    for item in data_list:
        # Check for common invalid values
        if item is None:
            invalid_count += 1
            continue
        
        if isinstance(item, str) and item.strip() == "":
            invalid_count += 1
            continue
        
        if isinstance(item, (int, float)) and (item < 0 or item > 1000):
            print(f"Warning: Unusual value {item} detected")
        
        cleaned.append(item)
    
    print(f"Removed {invalid_count} invalid values")
    return cleaned

# Test with messy data
messy_data = [10, None, 25, "", 50, -5, 1500, 30]
clean_result = clean_data(messy_data)
print(f"Original: {messy_data}")
print(f"Cleaned: {clean_result}\n")

# Example 3: Single data point edge case
print("3. Single Data Point Edge Cases:")
def calculate_average(numbers):
    """Calculate average handling edge cases"""
    if not numbers:
        print("Edge case: No numbers provided")
        return 0
    
    if len(numbers) == 1:
        print("Edge case: Only one number provided")
        return numbers[0]
    
    # Check for all zeros
    if all(num == 0 for num in numbers):
        print("Edge case: All values are zero")
        return 0
    
    return sum(numbers) / len(numbers)

# Test different edge cases
test_lists = [
    [],           # Empty
    [42],         # Single item
    [0, 0, 0],    # All zeros
    [1, 2, 3, 4]  # Normal case
]

for i, test_list in enumerate(test_lists):
    avg = calculate_average(test_list)
    print(f"List {i+1} {test_list}: Average = {avg}")
print()

# Example 4: Boundary value testing
print("4. Boundary Value Edge Cases:")
def validate_percentage(value):
    """Validate percentage values at boundaries"""
    try:
        # Convert to float if string
        if isinstance(value, str):
            value = float(value)
        
        # Check exact boundaries
        if value == 0:
            return "Exactly 0% - minimum boundary"
        elif value == 100:
            return "Exactly 100% - maximum boundary"
        elif value < 0:
            return "Below 0% - invalid!"
        elif value > 100:
            return "Above 100% - invalid!"
        else:
            return f"Valid: {value}%"
    
    except ValueError:
        return "Cannot convert to number!"

# Test boundary cases
boundary_tests = [-1, 0, 0.1, 50, 99.9, 100, 101, "50", "invalid"]
for test_val in boundary_tests:
    result = validate_percentage(test_val)
    print(f"Value {test_val}: {result}")