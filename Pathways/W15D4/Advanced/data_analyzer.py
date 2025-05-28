# Advanced Example 2: Student Grade Data Analyzer
# This combines all optimization techniques into a practical program

import time
import random
from collections import defaultdict

class StudentGradeAnalyzer:
    """
    Analyzes student grade data efficiently using all the optimization techniques
    we learned in the basic examples.
    """
    
    def __init__(self):
        # Use efficient data structures from the start
        self.grade_cache = {}
        self.student_lookup = {}  # Dictionary for fast student lookups
        self.subject_sets = defaultdict(set)  # Sets for fast membership testing
        
    def generate_sample_data(self, num_students=1000, num_grades_per_student=10):
        """Generate sample student data for testing"""
        print(f"Generating sample data for {num_students} students...")
        
        subjects = ["Math", "Science", "English", "History", "Art"]
        students = []
        
        # Use list comprehension for faster data generation
        for student_id in range(num_students):
            student_name = f"Student_{student_id:04d}"
            
            # Generate grades efficiently
            student_grades = [
                {
                    'subject': random.choice(subjects),
                    'grade': random.randint(60, 100),
                    'assignment': f"Assignment_{i}"
                }
                for i in range(num_grades_per_student)
            ]
            
            students.append({
                'id': student_id,
                'name': student_name,
                'grades': student_grades
            })
        
        return students
    
    def build_efficient_indexes(self, students):
        """Build indexes for fast data access - a key optimization technique"""
        print("Building efficient data indexes...")
        
        # Clear previous indexes
        self.student_lookup.clear()
        self.subject_sets.clear()
        
        # Build student lookup dictionary (O(1) access instead of O(n) searching)
        for student in students:
            self.student_lookup[student['id']] = student
            
            # Also build subject sets for each student
            for grade in student['grades']:
                self.subject_sets[student['id']].add(grade['subject'])
    
    def calculate_student_average_slow(self, student_id, students):
        """Slow way - search through all students every time"""
        # Bad: Linear search through all students
        student = None
        for s in students:
            if s['id'] == student_id:
                student = s
                break
        
        if not student:
            return None
        
        # Bad: Create new list and use sum()
        grades = []
        for grade in student['grades']:
            grades.append(grade['grade'])
        
        return sum(grades) / len(grades) if grades else 0
    
    def calculate_student_average_fast(self, student_id):
        """Fast way - use pre-built index and efficient calculation"""
        # Good: O(1) lookup using dictionary
        student = self.student_lookup.get(student_id)
        if not student:
            return None
        
        # Good: Calculate directly without creating intermediate lists
        total = sum(grade['grade'] for grade in student['grades'])
        count = len(student['grades'])
        
        return total / count if count > 0 else 0
    
    def find_top_students_slow(self, students, subject=None, top_n=10):
        """Slow way to find top students"""
        student_averages = []
        
        # Bad: Calculate average for every student every time
        for student in students:
            if subject:
                # Bad: Filter grades using a loop
                subject_grades = []
                for grade in student['grades']:
                    if grade['subject'] == subject:
                        subject_grades.append(grade['grade'])
                
                if subject_grades:
                    avg = sum(subject_grades) / len(subject_grades)
                else:
                    continue
            else:
                grades = [grade['grade'] for grade in student['grades']]
                avg = sum(grades) / len(grades) if grades else 0
            
            student_averages.append((student['name'], avg))
        
        # Bad: Sort the entire list
        student_averages.sort(key=lambda x: x[1], reverse=True)
        return student_averages[:top_n]
    
    def find_top_students_fast(self, subject=None, top_n=10):
        """Fast way using cached calculations and efficient filtering"""
        student_averages = []
        
        # Good: Use pre-built indexes
        for student_id, student in self.student_lookup.items():
            cache_key = (student_id, subject)
            
            # Check cache first
            if cache_key in self.grade_cache:
                avg = self.grade_cache[cache_key]
            else:
                if subject:
                    # Good: Use set membership for fast checking
                    if subject not in self.subject_sets[student_id]:
                        continue
                    
                    # Good: Use generator expression with filter
                    subject_grades = [g['grade'] for g in student['grades'] if g['subject'] == subject]
                    avg = sum(subject_grades) / len(subject_grades) if subject_grades else 0
                else:
                    avg = self.calculate_student_average_fast(student_id)
                
                # Cache the result
                self.grade_cache[cache_key] = avg
            
            if avg > 0:  # Only include students with grades
                student_averages.append((student['name'], avg))
        
        # Good: Use built-in sorted() which is optimized
        return sorted(student_averages, key=lambda x: x[1], reverse=True)[:top_n]
    
    def analyze_grade_distribution_slow(self, students, subject=None):
        """Slow grade distribution analysis"""
        all_grades = []
        
        # Bad: Multiple passes through data
        for student in students:
            for grade in student['grades']:
                if subject is None or grade['subject'] == subject:
                    all_grades.append(grade['grade'])
        
        if not all_grades:
            return {}
        
        # Bad: Multiple calculations that could be done in one pass
        return {
            'count': len(all_grades),
            'average': sum(all_grades) / len(all_grades),
            'min': min(all_grades),
            'max': max(all_grades),
            'a_grades': len([g for g in all_grades if g >= 90]),
            'b_grades': len([g for g in all_grades if 80 <= g < 90]),
            'c_grades': len([g for g in all_grades if 70 <= g < 80]),
            'failing': len([g for g in all_grades if g < 70])
        }
    
    def analyze_grade_distribution_fast(self, subject=None):
        """Fast grade distribution - calculate everything in one pass"""
        count = 0
        total = 0
        min_grade = float('inf')
        max_grade = float('-inf')
        a_count = b_count = c_count = fail_count = 0
        
        # Good: Single pass through data, calculate everything at once
        for student in self.student_lookup.values():
            for grade in student['grades']:
                if subject is None or grade['subject'] == subject:
                    grade_value = grade['grade']
                    count += 1
                    total += grade_value
                    
                    # Update min/max
                    if grade_value < min_grade:
                        min_grade = grade_value
                    if grade_value > max_grade:
                        max_grade = grade_value
                    
                    # Count grade categories
                    if grade_value >= 90:
                        a_count += 1
                    elif grade_value >= 80:
                        b_count += 1
                    elif grade_value >= 70:
                        c_count += 1
                    else:
                        fail_count += 1
        
        if count == 0:
            return {}
        
        return {
            'count': count,
            'average': total / count,
            'min': min_grade,
            'max': max_grade,
            'a_grades': a_count,
            'b_grades': b_count,
            'c_grades': c_count,
            'failing': fail_count
        }
    
    def run_performance_comparison(self, students):
        """Compare performance of slow vs fast methods"""
        print("\n=== Performance Comparison ===")
        
        # Test 1: Finding top students
        print("\n--- Finding Top 10 Students in Math ---")
        
        start_time = time.time()
        slow_top = self.find_top_students_slow(students, "Math", 10)
        slow_time = time.time() - start_time
        
        start_time = time.time()
        fast_top = self.find_top_students_fast("Math", 10)
        fast_time = time.time() - start_time
        
        print(f"Slow method: {slow_time:.4f} seconds")
        print(f"Fast method: {fast_time:.4f} seconds")
        print(f"Speed improvement: {slow_time/fast_time:.2f}x faster")
        
        # Test 2: Grade distribution analysis
        print("\n--- Analyzing Grade Distribution ---")
        
        start_time = time.time()
        slow_dist = self.analyze_grade_distribution_slow(students)
        slow_time = time.time() - start_time
        
        start_time = time.time()
        fast_dist = self.analyze_grade_distribution_fast()
        fast_time = time.time() - start_time
        
        print(f"Slow method: {slow_time:.4f} seconds")
        print(f"Fast method: {fast_time:.4f} seconds")
        print(f"Speed improvement: {slow_time/fast_time:.2f}x faster")
        
        # Show some results
        print(f"\n--- Sample Results ---")
        print(f"Top 3 Math students: {fast_top[:3]}")
        print(f"Overall grade distribution:")
        print(f"  Total grades: {fast_dist['count']}")
        print(f"  Average: {fast_dist['average']:.1f}")
        print(f"  A grades: {fast_dist['a_grades']}")
        print(f"  Failing grades: {fast_dist['failing']}")

# Demo the grade analyzer
if __name__ == "__main__":
    print("=== Student Grade Analyzer ===")
    print("Demonstrating performance optimization techniques")
    
    analyzer = StudentGradeAnalyzer()
    
    # Generate test data
    students = analyzer.generate_sample_data(num_students=2000, num_grades_per_student=15)
    
    # Build efficient indexes
    analyzer.build_efficient_indexes(students)
    
    # Run performance comparison
    analyzer.run_performance_comparison(students)
    
    print(f"\n🎯 Key Takeaways:")
    print(f"   1. Pre-calculate and cache what you can")
    print(f"   2. Use the right data structure (dict vs list, set vs list)")
    print(f"   3. Build indexes for data you'll search frequently")
    print(f"   4. Do calculations in one pass when possible")
    print(f"   5. Small optimizations add up to big improvements!")