# File 5: Advanced - Custom Exceptions and Logging
# Creating custom exceptions and implementing error logging

import logging
from datetime import datetime

print("=== Custom Exceptions and Error Logging ===\n")

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error_log.txt'),
        logging.StreamHandler()  # Also print to console
    ]
)

# Custom Exception Classes
class StudentGradeError(Exception):
    """Custom exception for student grade validation"""
    def __init__(self, message, grade_value=None):
        super().__init__(message)
        self.grade_value = grade_value
        self.timestamp = datetime.now()

class InsufficientFundsError(Exception):
    """Custom exception for banking operations"""
    def __init__(self, message, attempted_amount, current_balance):
        super().__init__(message)
        self.attempted_amount = attempted_amount
        self.current_balance = current_balance

class InvalidEmailError(Exception):
    """Custom exception for email validation"""
    pass

# Student Grade Management System
class GradeManager:
    """Manages student grades with custom error handling"""
    
    def __init__(self):
        self.students = {}
        self.logger = logging.getLogger('GradeManager')
    
    def add_grade(self, student_name, grade):
        """Add a grade for a student with validation"""
        try:
            # Validate grade range
            if not isinstance(grade, (int, float)):
                raise StudentGradeError(
                    f"Grade must be a number, got {type(grade).__name__}",
                    grade
                )
            
            if grade < 0 or grade > 100:
                raise StudentGradeError(
                    f"Grade must be between 0 and 100, got {grade}",
                    grade
                )
            
            # Add grade
            if student_name not in self.students:
                self.students[student_name] = []
            
            self.students[student_name].append(grade)
            self.logger.info(f"Added grade {grade} for {student_name}")
            print(f"Successfully added grade {grade} for {student_name}")
            
        except StudentGradeError as e:
            error_msg = f"Grade Error for {student_name}: {e}"
            self.logger.error(error_msg)
            print(error_msg)
            
            # Log additional details if available
            if hasattr(e, 'grade_value') and e.grade_value is not None:
                self.logger.error(f"Invalid grade value: {e.grade_value}")
        
        except Exception as e:
            error_msg = f"Unexpected error adding grade for {student_name}: {e}"
            self.logger.critical(error_msg)
            print(error_msg)
    
    def get_average(self, student_name):
        """Get average grade with error handling"""
        try:
            if student_name not in self.students:
                raise StudentGradeError(f"Student {student_name} not found")
            
            grades = self.students[student_name]
            if not grades:
                raise StudentGradeError(f"No grades found for {student_name}")
            
            average = sum(grades) / len(grades)
            self.logger.info(f"Calculated average for {student_name}: {average:.2f}")
            return average
            
        except StudentGradeError as e:
            self.logger.warning(f"Grade calculation error: {e}")
            print(f"Error: {e}")
            return None

# Simple Banking System with Custom Exceptions
class BankAccount:
    """Simple bank account with custom error handling"""
    
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.logger = logging.getLogger('BankAccount')
        
        self.logger.info(f"Account created for {account_holder} with balance ${initial_balance}")
    
    def withdraw(self, amount):
        """Withdraw money with custom exception handling"""
        try:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive")
            
            if amount > self.balance:
                raise InsufficientFundsError(
                    f"Cannot withdraw ${amount}. Insufficient funds.",
                    amount,
                    self.balance
                )
            
            self.balance -= amount
            self.logger.info(f"{self.account_holder} withdrew ${amount}. New balance: ${self.balance}")
            print(f"Withdrawal successful. New balance: ${self.balance}")
            
        except InsufficientFundsError as e:
            error_msg = f"Transaction failed: {e}"
            self.logger.warning(error_msg)
            print(error_msg)
            print(f"Available balance: ${e.current_balance}")
            
        except ValueError as e:
            error_msg = f"Invalid withdrawal amount: {e}"
            self.logger.error(error_msg)
            print(error_msg)
        
        except Exception as e:
            error_msg = f"Unexpected error during withdrawal: {e}"
            self.logger.critical(error_msg)
            print(error_msg)

# Email Validation System
def validate_email(email):
    """Validate email with custom exceptions and logging"""
    logger = logging.getLogger('EmailValidator')
    
    try:
        if not email or not isinstance(email, str):
            raise InvalidEmailError("Email cannot be empty or non-string")
        
        email = email.strip()
        
        if '@' not in email:
            raise InvalidEmailError("Email must contain @ symbol")
        
        if email.count('@') != 1:
            raise InvalidEmailError("Email must contain exactly one @")
        
        username, domain = email.split('@')
        
        if not username or not domain:
            raise InvalidEmailError("Email must have both username and domain")
        
        if '.' not in domain:
            raise InvalidEmailError("Domain must contain at least one dot")
        
        logger.info(f"Email validation successful: {email}")
        print(f"Valid email: {email}")
        return True
        
    except InvalidEmailError as e:
        error_msg = f"Email validation failed: {e}"
        logger.warning(error_msg)
        print(error_msg)
        return False
    
    except Exception as e:
        error_msg = f"Unexpected error validating email: {e}"
        logger.error(error_msg)
        print(error_msg)
        return False

# Demonstration
if __name__ == "__main__":
    print("=== Testing Custom Exceptions ===\n")
    
    # Test Grade Manager
    print("1. Testing Grade Manager:")
    grade_mgr = GradeManager()
    grade_mgr.add_grade("Alice", 85)
    grade_mgr.add_grade("Bob", 150)  # Invalid grade
    grade_mgr.add_grade("Charlie", "A")  # Invalid type
    print(f"Alice's average: {grade_mgr.get_average('Alice')}")
    print(f"David's average: {grade_mgr.get_average('David')}")  # Student not found
    
    print("\n" + "="*50)
    
    # Test Bank Account
    print("2. Testing Bank Account:")
    account = BankAccount("John Doe", 100)
    account.withdraw(50)   # Valid withdrawal
    account.withdraw(100)  # Insufficient funds
    account.withdraw(-20)  # Invalid amount
    
    print("\n" + "="*50)
    
    # Test Email Validation
    print("3. Testing Email Validation:")
    emails = [
        "user@example.com",      # Valid
        "invalid.email",         # No @
        "user@@domain.com",      # Multiple @
        "@domain.com",           # No username
        "user@",                 # No domain
        "user@domain",           # No dot in domain
        ""                       # Empty
    ]
    
    for email in emails:
        validate_email(email)
    
    print(f"\nCheck 'error_log.txt' for detailed logging information!")