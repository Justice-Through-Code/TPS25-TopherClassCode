# Basic Refactoring Example 2: Improving Variable Names
# This shows how good variable names make code much clearer

print("=== BEFORE REFACTORING ===")
print("Code with confusing variable names:")

# Bad variable names - hard to understand
x = 10
y = 5
z = x * y
if z > 30:
    result = "big"
else:
    result = "small"
print(f"x={x}, y={y}, z={z}, result={result}")

print("\n=== AFTER REFACTORING ===")
print("Code with clear variable names:")

# Good variable names - easy to understand
length = 10
width = 5
area = length * width
if area > 30:
    size_category = "big"
else:
    size_category = "small"
print(f"length={length}, width={width}, area={area}, size={size_category}")

print("\n=== MORE EXAMPLES ===")

# Before: confusing names
print("Before - confusing:")
data = [85, 92, 78, 96, 88]
total = 0
for item in data:
    total += item
avg = total / len(data)
print(f"Average: {avg}")

print("\nAfter - clear names:")
# After: clear names
test_scores = [85, 92, 78, 96, 88]
total_points = 0
for score in test_scores:
    total_points += score
average_score = total_points / len(test_scores)
print(f"Average test score: {average_score}")

print("\n=== NAMING RULES FOR BEGINNERS ===")
print("✓ Use full words, not abbreviations (score not sc)")
print("✓ Be specific (student_name not name)")
print("✓ Use snake_case for variables (total_score)")
print("✓ Make names explain what the variable contains")