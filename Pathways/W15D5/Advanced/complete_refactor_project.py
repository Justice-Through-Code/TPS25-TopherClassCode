# Advanced Refactoring Example 2: Complete Application
# This builds on ALL previous examples to create a full, robust application

print("=== COMPLETE REFACTORED APPLICATION ===")
print("This combines all refactoring concepts we've learned!")

import json
from typing import List, Dict, Optional

class Grade:
    """Represents a single grade with validation"""
    
    def __init__(self, subject: str, score: float):
        """Create a grade with validation"""
        self.subject = self._validate_subject(subject)
        self.score = self._validate_score(score)
    
    def _validate_subject(self, subject: str) -> str:
        """Ensure subject name is valid"""
        if not subject or not subject.strip():
            raise ValueError("Subject name cannot be empty")
        return subject.strip().title()
    
    def _validate_score(self, score: float) -> float:
        """Ensure score is within valid range"""
        if not isinstance(score, (int, float)):
            raise TypeError("Score must be a number")
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")
        return float(score)
    
    def __str__(self):
        """String representation of grade"""
        return f"{self.subject}: {self.score}"


class Student:
    """Enhanced student class with error handling and data persistence"""
    
    def __init__(self, name: str, student_id: Optional[str] = None):
        """Create a student with validation"""
        self.name = self._validate_name(name)
        self.student_id = student_id or self._generate_id()
        self.grades: List[Grade] = []
    
    def _validate_name(self, name: str) -> str:
        """Ensure student name is valid"""
        if not name or not name.strip():
            raise ValueError("Student name cannot be empty")
        return name.strip().title()
    
    def _generate_id(self) -> str:
        """Generate a simple student ID"""
        import random
        return f"STU{random.randint(1000, 9999)}"
    
    def add_grade(self, subject: str, score: float) -> bool:
        """Add a grade with error handling"""
        try:
            new_grade = Grade(subject, score)
            
            # Check if grade already exists for this subject
            for i, existing_grade in enumerate(self.grades):
                if existing_grade.subject == new_grade.subject:
                    print(f"Updating existing {subject} grade from {existing_grade.score} to {score}")
                    self.grades[i] = new_grade
                    return True
            
            # Add new grade
            self.grades.append(new_grade)
            print(f"Added {subject} grade of {score} for {self.name}")
            return True
            
        except (ValueError, TypeError) as error:
            print(f"Error adding grade: {error}")
            return False
    
    def calculate_average(self) -> float:
        """Calculate average with error handling"""
        if not self.grades:
            return 0.0
        
        total_points = sum(grade.score for grade in self.grades)
        return round(total_points / len(self.grades), 2)
    
    def get_letter_grade(self) -> str:
        """Convert average to letter grade"""
        average = self.calculate_average()
        
        grade_scale = [
            (97, "A+"), (93, "A"), (90, "A-"),
            (87, "B+"), (83, "B"), (80, "B-"),
            (77, "C+"), (73, "C"), (70, "C-"),
            (67, "D+"), (63, "D"), (60, "D-"),
            (0, "F")
        ]
        
        for min_score, letter in grade_scale:
            if average >= min_score:
                return letter
        return "F"
    
    def get_grades_by_subject(self) -> Dict[str, float]:
        """Get all grades organized by subject"""
        return {grade.subject: grade.score for grade in self.grades}
    
    def display_transcript(self):
        """Display detailed student transcript"""
        print(f"\n{'='*50}")
        print(f"OFFICIAL TRANSCRIPT")
        print(f"Student: {self.name} (ID: {self.student_id})")
        print(f"{'='*50}")
        
        if not self.grades:
            print("No grades recorded yet.")
            return
        
        # Display individual grades
        print("COURSE GRADES:")
        print("-" * 30)
        for grade in sorted(self.grades, key=lambda g: g.subject):
            print(f"{grade.subject:.<20} {grade.score:>6.1f}")
        
        # Display summary
        print("-" * 30)
        average = self.calculate_average()
        letter_grade = self.get_letter_grade()
        print(f"{'GPA':.<20} {average:>6.2f}")
        print(f"{'Letter Grade':.<20} {letter_grade:>6}")
        print("=" * 50)
    
    def to_dict(self) -> Dict:
        """Convert student to dictionary for saving"""
        return {
            'name': self.name,
            'student_id': self.student_id,
            'grades': [{'subject': g.subject, 'score': g.score} for g in self.grades]
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create student from dictionary"""
        student = cls(data['name'], data['student_id'])
        for grade_data in data['grades']:
            student.add_grade(grade_data['subject'], grade_data['score'])
        return student


class GradeManager:
    """Advanced classroom management system"""
    
    def __init__(self, class_name: str):
        """Initialize the grade management system"""
        self.class_name = class_name
        self.students: Dict[str, Student] = {}
    
    def add_student(self, name: str) -> Optional[Student]:
        """Add a new student with error handling"""
        try:
            student = Student(name)
            self.students[student.student_id] = student
            print(f"Successfully added {student.name} (ID: {student.student_id})")
            return student
        except ValueError as error:
            print(f"Error adding student: {error}")
            return None
    
    def find_student(self, identifier: str) -> Optional[Student]:
        """Find student by name or ID"""
        # Try to find by ID first
        if identifier in self.students:
            return self.students[identifier]
        
        # Then try to find by name
        for student in self.students.values():
            if student.name.lower() == identifier.lower():
                return student
        
        return None
    
    def add_grade_to_student(self, student_identifier: str, subject: str, score: float) -> bool:
        """Add grade to specific student"""
        student = self.find_student(student_identifier)
        if not student:
            print(f"Student '{student_identifier}' not found")
            return False
        
        return student.add_grade(subject, score)
    
    def display_class_report(self):
        """Display comprehensive class report"""
        print(f"\n{'='*60}")
        print(f"CLASS REPORT: {self.class_name}")
        print(f"{'='*60}")
        
        if not self.students:
            print("No students enrolled in this class.")
            return
        
        students_list = list(self.students.values())
        students_list.sort(key=lambda s: s.calculate_average(), reverse=True)
        
        print(f"{'Rank':<6} {'Name':<20} {'ID':<10} {'Average':<8} {'Grade'}")
        print("-" * 60)
        
        for rank, student in enumerate(students_list, 1):
            avg = student.calculate_average()
            grade = student.get_letter_grade()
            print(f"{rank:<6} {student.name:<20} {student.student_id:<10} {avg:<8.2f} {grade}")
        
        # Class statistics
        class_average = sum(s.calculate_average() for s in students_list) / len(students_list)
        print("-" * 60)
        print(f"Class Average: {class_average:.2f}")
        print(f"Total Students: {len(students_list)}")
    
    def save_to_file(self, filename: str) -> bool:
        """Save class data to JSON file"""
        try:
            data = {
                'class_name': self.class_name,
                'students': [student.to_dict() for student in self.students.values()]
            }
            with open(filename, 'w') as file:
                json.dump(data, file, indent=2)
            print(f"Class data saved to {filename}")
            return True
        except Exception as error:
            print(f"Error saving file: {error}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """Load class data from JSON file"""
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
            
            self.class_name = data['class_name']
            self.students = {}
            
            for student_data in data['students']:
                student = Student.from_dict(student_data)
                self.students[student.student_id] = student
            
            print(f"Class data loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except Exception as error:
            print(f"Error loading file: {error}")
            return False


# Demonstration of the complete refactored system
def main():
    """Demonstrate the complete grade management system"""
    print("=== COMPLETE GRADE MANAGEMENT SYSTEM DEMO ===")
    
    # Create grade manager
    grade_manager = GradeManager("Computer Science 101")
    
    # Add students
    students_data = [
        ("Alice Johnson", [("Python", 92), ("Math", 88), ("English", 85)]),
        ("Bob Smith", [("Python", 78), ("Math", 82), ("English", 90)]),
        ("Carol Davis", [("Python", 95), ("Math", 91), ("English", 87)]),
    ]
    
    for name, grades in students_data:
        student = grade_manager.add_student(name)
        if student:
            for subject, score in grades:
                student.add_grade(subject, score)
    
    # Display individual transcripts
    for student in grade_manager.students.values():
        student.display_transcript()
    
    # Display class report
    grade_manager.display_class_report()
    
    # Demonstrate error handling
    print("\n=== ERROR HANDLING DEMO ===")
    grade_manager.add_grade_to_student("Alice Johnson", "History", 105)  # Invalid score
    grade_manager.add_grade_to_student("NonExistent", "Math", 85)  # Student not found
    
    print("\n=== ALL REFACTORING PRINCIPLES DEMONSTRATED ===")
    print("✓ Clean function and variable names")
    print("✓ No code duplication")
    print("✓ Well-organized classes")
    print("✓ Error handling and validation")
    print("✓ Type hints for clarity")
    print("✓ Data persistence (save/load)")
    print("✓ Comprehensive documentation")
    print("✓ Separation of concerns")

if __name__ == "__main__":
    main()