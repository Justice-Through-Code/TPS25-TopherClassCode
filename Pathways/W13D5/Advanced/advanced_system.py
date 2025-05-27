# advanced_system.py
# Advanced example building on previous files - Student Management System

import random
import datetime
from typing import List, Dict, Optional

# Import concepts from previous files
class DataProcessor:
    """Advanced data processing using techniques from basic_functions.py"""
    
    @staticmethod
    def calculate_grade(score, max_score=100):
        """Calculate letter grade from numeric score"""
        percentage = (score / max_score) * 100
        
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    @staticmethod
    def format_student_name(first_name, last_name):
        """Format student name consistently"""
        return f"{last_name.upper()}, {first_name.title()}"
    
    @staticmethod
    def calculate_statistics(scores: List[float]) -> Dict:
        """Calculate statistical measures for a list of scores"""
        if not scores:
            return {"error": "No scores provided"}
        
        avg = sum(scores) / len(scores)
        sorted_scores = sorted(scores)
        median = sorted_scores[len(scores) // 2]
        
        return {
            "average": round(avg, 2),
            "median": median,
            "highest": max(scores),
            "lowest": min(scores),
            "count": len(scores)
        }

class Student:
    """Advanced student class building on simple_classes.py concepts"""
    
    def __init__(self, student_id: int, first_name: str, last_name: str, grade_level: int):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.grade_level = grade_level
        self.assignments = {}  # assignment_name: score
        self.attendance = []   # list of date strings
        self.processor = DataProcessor()
    
    @property
    def full_name(self):
        """Property that uses DataProcessor for consistent formatting"""
        return self.processor.format_student_name(self.first_name, self.last_name)
    
    def add_assignment(self, assignment_name: str, score: float, max_score: float = 100):
        """Add an assignment score"""
        self.assignments[assignment_name] = {
            "score": score,
            "max_score": max_score,
            "letter_grade": self.processor.calculate_grade(score, max_score),
            "date_submitted": datetime.datetime.now().strftime("%Y-%m-%d")
        }
    
    def mark_attendance(self, date: str, present: bool = True):
        """Mark attendance for a specific date"""
        self.attendance.append({
            "date": date,
            "present": present
        })
    
    def get_grade_summary(self) -> Dict:
        """Get comprehensive grade summary using DataProcessor"""
        if not self.assignments:
            return {"message": "No assignments recorded"}
        
        scores = [assignment["score"] for assignment in self.assignments.values()]
        max_scores = [assignment["max_score"] for assignment in self.assignments.values()]
        
        # Calculate percentages for each assignment
        percentages = [(score/max_score)*100 for score, max_score in zip(scores, max_scores)]
        
        stats = self.processor.calculate_statistics(percentages)
        overall_grade = self.processor.calculate_grade(stats["average"])
        
        return {
            "student": self.full_name,
            "overall_grade": overall_grade,
            "statistics": stats,
            "assignment_count": len(self.assignments)
        }

class Classroom:
    """Advanced classroom management integrating multiple components"""
    
    def __init__(self, class_name: str, teacher_name: str):
        self.class_name = class_name
        self.teacher_name = teacher_name
        self.students: Dict[int, Student] = {}
        self.processor = DataProcessor()
        self.class_assignments = []  # Track all assignments given to class
    
    def enroll_student(self, student: Student):
        """Enroll a student in the classroom"""
        self.students[student.student_id] = student
        print(f"Enrolled {student.full_name} in {self.class_name}")
    
    def assign_homework(self, assignment_name: str, max_score: float = 100):
        """Assign homework to all students and simulate random completion"""
        self.class_assignments.append({
            "name": assignment_name,
            "max_score": max_score,
            "assigned_date": datetime.datetime.now().strftime("%Y-%m-%d")
        })
        
        print(f"\nAssigning '{assignment_name}' to all students...")
        
        for student in self.students.values():
            # Simulate random score (70-100% range for realistic grades)
            random_percentage = random.uniform(0.70, 1.0)
            score = random_percentage * max_score
            student.add_assignment(assignment_name, round(score, 1), max_score)
    
    def take_attendance(self, date: str):
        """Take attendance for all students with some random absences"""
        print(f"\nTaking attendance for {date}:")
        
        for student in self.students.values():
            # 90% chance of being present
            present = random.random() > 0.1
            student.mark_attendance(date, present)
            status = "Present" if present else "Absent"
            print(f"  {student.full_name}: {status}")
    
    def generate_class_report(self) -> str:
        """Generate comprehensive class report integrating all components"""
        if not self.students:
            return "No students enrolled in class."
        
        # Collect all student data
        student_summaries = []
        all_percentages = []
        
        for student in self.students.values():
            summary = student.get_grade_summary()
            if "statistics" in summary:
                student_summaries.append(summary)
                all_percentages.append(summary["statistics"]["average"])
        
        # Calculate class-wide statistics
        class_stats = self.processor.calculate_statistics(all_percentages) if all_percentages else {}
        
        # Build comprehensive report
        report_lines = [
            "="*60,
            f"CLASS REPORT: {self.class_name}",
            f"Teacher: {self.teacher_name}",
            f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "="*60,
            "",
            f"ENROLLMENT: {len(self.students)} students",
            f"ASSIGNMENTS GIVEN: {len(self.class_assignments)}",
            "",
            "INDIVIDUAL STUDENT PERFORMANCE:",
            "-"*40
        ]
        
        # Add individual student performance
        for summary in sorted(student_summaries, key=lambda x: x["statistics"]["average"], reverse=True):
            report_lines.extend([
                f"Student: {summary['student']}",
                f"  Overall Grade: {summary['overall_grade']}",
                f"  Average: {summary['statistics']['average']}%",
                f"  Assignments Completed: {summary['assignment_count']}",
                ""
            ])
        
        # Add class statistics
        if class_stats:
            report_lines.extend([
                "CLASS STATISTICS:",
                "-"*40,
                f"Class Average: {class_stats['average']}%",
                f"Highest Student Average: {class_stats['highest']}%",
                f"Lowest Student Average: {class_stats['lowest']}%",
                f"Median: {class_stats['median']}%",
                ""
            ])
        
        # Add assignment summary
        report_lines.extend([
            "ASSIGNMENTS GIVEN:",
            "-"*40
        ])
        
        for assignment in self.class_assignments:
            report_lines.append(f"• {assignment['name']} (Max: {assignment['max_score']} pts) - {assignment['assigned_date']}")
        
        return "\n".join(report_lines)

# Example usage demonstrating advanced integration
if __name__ == "__main__":
    print("Creating Advanced Student Management System...")
    print("This builds on concepts from all previous files!\n")
    
    # Create classroom
    math_class = Classroom("Advanced Algebra", "Ms. Johnson")
    
    # Create and enroll students
    students_data = [
        (101, "Alice", "Smith", 10),
        (102, "Bob", "Johnson", 10),
        (103, "Charlie", "Brown", 10),
        (104, "Diana", "Wilson", 10),
        (105, "Eve", "Davis", 10)
    ]
    
    for student_id, first, last, grade in students_data:
        student = Student(student_id, first, last, grade)
        math_class.enroll_student(student)
    
    # Simulate class activities over time
    print("\nSimulating class activities...")
    
    # Week 1
    math_class.take_attendance("2024-01-15")
    math_class.assign_homework("Quadratic Equations", 50)
    
    # Week 2  
    math_class.take_attendance("2024-01-22")
    math_class.assign_homework("Polynomial Factoring", 75)
    
    # Week 3
    math_class.take_attendance("2024-01-29")
    math_class.assign_homework("Systems of Equations", 100)
    
    # Generate and display comprehensive report
    print("\n" + "="*60)
    print("GENERATING COMPREHENSIVE CLASS REPORT")
    print("="*60)
    
    report = math_class.generate_class_report()
    print(report)