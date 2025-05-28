# Advanced Refactoring Example 1: Using Classes for Better Organization
# This builds on our previous examples by organizing related data and functions together

print("=== BUILDING ON PREVIOUS EXAMPLES ===")
print("Taking our student grade system and making it even better with classes")

# This combines concepts from our previous examples:
# - Good function names (from example 1)
# - Clear variable names (from example 2)  
# - No code duplication (from example 3)

class Student:
    """A class to represent a student and their grades"""
    
    def __init__(self, name):
        """Create a new student with a name"""
        self.name = name
        self.grades = {}  # Dictionary to store subject grades
    
    def add_grade(self, subject, score):
        """Add a grade for a specific subject"""
        self.grades[subject] = score
        print(f"Added {subject} grade of {score} for {self.name}")
    
    def calculate_average(self):
        """Calculate the average of all grades"""
        if not self.grades:  # No grades yet
            return 0
        
        total_points = sum(self.grades.values())
        number_of_subjects = len(self.grades)
        return total_points / number_of_subjects
    
    def get_letter_grade(self):
        """Get letter grade based on average"""
        average_score = self.calculate_average()
        
        if average_score >= 90:
            return "A"
        elif average_score >= 80:
            return "B"
        elif average_score >= 70:
            return "C"
        elif average_score >= 60:
            return "D"
        else:
            return "F"
    
    def display_report_card(self):
        """Display complete student report"""
        print(f"\n--- Report Card for {self.name} ---")
        
        # Show individual grades
        for subject, score in self.grades.items():
            print(f"{subject}: {score}")
        
        # Show average and letter grade
        average_score = self.calculate_average()
        letter_grade = self.get_letter_grade()
        print(f"Average: {average_score:.1f}")
        print(f"Letter Grade: {letter_grade}")


class Classroom:
    """A class to manage multiple students"""
    
    def __init__(self, class_name):
        """Create a new classroom"""
        self.class_name = class_name
        self.students = []
    
    def add_student(self, student):
        """Add a student to the classroom"""
        self.students.append(student)
        print(f"{student.name} added to {self.class_name}")
    
    def display_class_summary(self):
        """Show summary of all students in class"""
        print(f"\n=== {self.class_name} Summary ===")
        
        if not self.students:
            print("No students in this class yet.")
            return
        
        total_class_average = 0
        for student in self.students:
            student_average = student.calculate_average()
            print(f"{student.name}: {student_average:.1f} ({student.get_letter_grade()})")
            total_class_average += student_average
        
        class_average = total_class_average / len(self.students)
        print(f"\nClass Average: {class_average:.1f}")


# Using our refactored system
print("\n=== DEMONSTRATION ===")

# Create a classroom
math_class = Classroom("Algebra 1")

# Create students (building on our previous examples)
john = Student("John")
john.add_grade("Math", 85)
john.add_grade("English", 92)
john.add_grade("Science", 78)

sarah = Student("Sarah")
sarah.add_grade("Math", 78)
sarah.add_grade("English", 84)
sarah.add_grade("Science", 91)

mike = Student("Mike")
mike.add_grade("Math", 94)
mike.add_grade("English", 88)
mike.add_grade("Science", 96)

# Add students to classroom
math_class.add_student(john)
math_class.add_student(sarah)
math_class.add_student(mike)

# Display individual report cards
john.display_report_card()
sarah.display_report_card()
mike.display_report_card()

# Display class summary
math_class.display_class_summary()

print("\n=== WHY CLASSES MAKE CODE BETTER ===")
print("✓ Related data and functions are grouped together")
print("✓ Each student manages their own grades")
print("✓ Easy to create many students without duplicating code")
print("✓ Code is organized and easier to understand")
print("✓ Can add new features easily (like classroom management)")