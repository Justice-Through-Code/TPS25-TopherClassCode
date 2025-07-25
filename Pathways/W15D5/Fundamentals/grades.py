student1_name = "Alice"
student1_math = 85
student1_english = 92
student1_science = 78

student2_name = "Bob"
student2_math = 90
student2_english = 88
student2_science = 95

student3_name = "Charlie"
student3_math = 76
student3_english = 84
student3_science = 89

def calculate_average_student1():
    avg = (student1_math + student1_english + student1_science) / 3
    print(student1_name + "'s average: " + str(avg))
    return avg

def calculate_average_student2():
    avg = (student2_math + student2_english + student2_science) / 3
    print(student2_name + "'s average: " + str(avg))
    return avg

def calculate_average_student3():
    avg = (student3_math + student3_english + student3_science) / 3
    print(student3_name + "'s average: " + str(avg))
    return avg

calculate_average_student1()
calculate_average_student2()
calculate_average_student3()