# File 4: Advanced - Input Validation System
# Building a robust user input validation system using error handling

print("=== Advanced Input Validation System ===\n")

class InputValidator:
    """A class to handle various input validation scenarios"""
    
    @staticmethod
    def get_integer_input(prompt, min_value=None, max_value=None):
        """Get valid integer input from user with optional range checking"""
        while True:
            try:
                user_input = input(prompt)
                number = int(user_input)
                
                # Range validation
                if min_value is not None and number < min_value:
                    raise ValueError(f"Number must be at least {min_value}")
                
                if max_value is not None and number > max_value:
                    raise ValueError(f"Number must be no more than {max_value}")
                
                return number
                
            except ValueError as e:
                if "invalid literal" in str(e):
                    print("Error: Please enter a valid integer")
                else:
                    print(f"Error: {e}")
                print("Please try again.\n")
    
    @staticmethod
    def get_choice_input(prompt, valid_choices):
        """Get user choice from a list of valid options"""
        while True:
            try:
                choice = input(prompt).strip().lower()
                
                if not choice:
                    raise ValueError("Input cannot be empty")
                
                if choice not in [str(c).lower() for c in valid_choices]:
                    raise ValueError(f"Please choose from: {', '.join(map(str, valid_choices))}")
                
                return choice
                
            except ValueError as e:
                print(f"Error: {e}")
                print("Please try again.\n")
    
    @staticmethod
    def get_float_input(prompt, positive_only=False):
        """Get valid float input with optional positive number requirement"""
        while True:
            try:
                user_input = input(prompt)
                number = float(user_input)
                
                if positive_only and number <= 0:
                    raise ValueError("Number must be positive")
                
                return number
                
            except ValueError as e:
                if "could not convert" in str(e):
                    print("Error: Please enter a valid number")
                else:
                    print(f"Error: {e}")
                print("Please try again.\n")

# Example usage of the validation system
def calculator_with_validation():
    """Calculator that uses robust input validation"""
    print("=== Robust Calculator ===")
    
    try:
        # Get first number
        num1 = InputValidator.get_float_input("Enter the first number: ")
        
        # Get operation
        operation = InputValidator.get_choice_input(
            "Choose operation (+, -, *, /): ",
            ['+', '-', '*', '/']
        )
        
        # Get second number
        num2 = InputValidator.get_float_input("Enter the second number: ")
        
        # Special handling for division
        if operation == '/' and num2 == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        
        # Perform calculation
        operations = {
            '+': num1 + num2,
            '-': num1 - num2,
            '*': num1 * num2,
            '/': num1 / num2
        }
        
        result = operations[operation]
        print(f"\nResult: {num1} {operation} {num2} = {result}")
        
    except ZeroDivisionError as e:
        print(f"Calculation error: {e}")
    except KeyboardInterrupt:
        print("\n\nCalculator interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    finally:
        print("Calculator session ended")

# Example of handling file operations with validation
def safe_file_processor():
    """Process files with comprehensive error handling"""
    print("\n=== Safe File Processor ===")
    
    filename = input("Enter filename to process: ").strip()
    
    if not filename:
        print("Error: Filename cannot be empty")
        return
    
    try:
        # Simulate file processing with various potential errors
        print(f"Processing file: {filename}")
        
        # Check file extension
        if not filename.endswith('.txt'):
            raise ValueError("Only .txt files are supported")
        
        # Simulate file size check
        if 'large' in filename.lower():
            raise MemoryError("File too large to process")
        
        # Simulate permission error
        if 'protected' in filename.lower():
            raise PermissionError("Access denied to file")
        
        # If we get here, file processing succeeded
        print("File processed successfully!")
        return True
        
    except ValueError as e:
        print(f"File format error: {e}")
    except FileNotFoundError:
        print("Error: File not found")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except MemoryError as e:
        print(f"Resource error: {e}")
    except Exception as e:
        print(f"Unexpected error during file processing: {e}")
    
    return False

# Demonstration (commented out for file usage)
print("This module provides InputValidator class and example functions:")
print("- InputValidator.get_integer_input()")
print("- InputValidator.get_choice_input()")  
print("- InputValidator.get_float_input()")
print("- calculator_with_validation()")
print("- safe_file_processor()")
print("\nUncomment the lines below to run interactive examples:")
print("# calculator_with_validation()")
print("# safe_file_processor()")