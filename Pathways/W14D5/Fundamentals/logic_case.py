# Buggy code - trying to find the average of a list
def find_average(numbers):
    total = 0
    for num in numbers:
        total = total + num
    average = total / len(numbers)  
    return average

# Test it
my_list = []
result = find_average(my_list)
print(result)  # This will crash!