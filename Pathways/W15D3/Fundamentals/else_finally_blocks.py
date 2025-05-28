# File 3: Else and Finally Blocks
# Using else and finally for complete error handling

print("=== Else and Finally Blocks ===\n")

# Example 1: Using else block (runs when no exception occurs)
print("Example 1: Using else block")
def divide_numbers(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None
    else:
        print("Division successful!")
        return result

print("Testing division:")
print(f"10 / 2 = {divide_numbers(10, 2)}")  # else block runs
print(f"10 / 0 = {divide_numbers(10, 0)}")  # else block doesn't run

print()

# Example 2: Using finally block (always runs)
print("Example 2: Using finally block")
def read_file_info(filename):
    file_handle = None
    try:
        print(f"Attempting to open {filename}")
        # Simulating file operations
        if filename == "missing.txt":
            raise FileNotFoundError("File not found")
        else:
            print(f"Successfully opened {filename}")
            return f"File {filename} processed"
    
    except FileNotFoundError:
        print("Error: Could not find the file")
        return "File processing failed"
    
    finally:
        print("Cleanup: Closing file resources")
        # In real code, you'd close file handles here
        print("Resources cleaned up\n")

# Test both success and failure cases
read_file_info("data.txt")
read_file_info("missing.txt")

# Example 3: Complete try-except-else-finally structure
print("Example 3: Complete structure (try-except-else-finally)")
def process_number_list(numbers):
    try:
        print("Starting number processing...")
        total = sum(numbers)
        average = total / len(numbers)
    
    except TypeError:
        print("Error: Invalid data type in list")
        return None
    
    except ZeroDivisionError:
        print("Error: Empty list provided")
        return None
    
    else:
        print("Processing completed successfully!")
        return {"total": total, "average": average}
    
    finally:
        print("Finished processing attempt")

# Test different scenarios
print("\nTest 1 - Valid numbers:")
result1 = process_number_list([1, 2, 3, 4, 5])
print(f"Result: {result1}")

print("\nTest 2 - Empty list:")
result2 = process_number_list([])
print(f"Result: {result2}")

print("\nTest 3 - Invalid data:")
result3 = process_number_list([1, 2, "three"])
print(f"Result: {result3}")