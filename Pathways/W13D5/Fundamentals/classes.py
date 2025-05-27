# simple_classes.py
# Basic example of integrating simple classes together

class Calculator:
    """A simple calculator class with basic operations"""
    
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
    
    def divide(self, a, b):
        if b == 0:
            return "Error: Cannot divide by zero"
        return a / b

class NumberFormatter:
    """A class to format numbers in different ways"""
    
    def format_currency(self, amount):
        return f"${amount:.2f}"
    
    def format_percentage(self, decimal):
        return f"{decimal * 100:.1f}%"
    
    def format_rounded(self, number, places=2):
        return round(number, places)

class MathProcessor:
    """Integration class that uses Calculator and NumberFormatter together"""
    
    def __init__(self):
        self.calc = Calculator()
        self.formatter = NumberFormatter()
    
    def calculate_tip(self, bill_amount, tip_percentage):
        """Calculate tip and format results"""
        # Convert percentage to decimal
        tip_decimal = tip_percentage / 100
        
        # Calculate tip amount using Calculator
        tip_amount = self.calc.multiply(bill_amount, tip_decimal)
        
        # Calculate total using Calculator
        total = self.calc.add(bill_amount, tip_amount)
        
        # Format results using NumberFormatter
        formatted_bill = self.formatter.format_currency(bill_amount)
        formatted_tip = self.formatter.format_currency(tip_amount)
        formatted_total = self.formatter.format_currency(total)
        formatted_percentage = self.formatter.format_percentage(tip_decimal)
        
        return {
            "bill": formatted_bill,
            "tip": formatted_tip,
            "total": formatted_total,
            "tip_rate": formatted_percentage
        }

# Example usage
if __name__ == "__main__":
    # Testing individual classes
    print("Testing Calculator:")
    calc = Calculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    
    print("\nTesting NumberFormatter:")
    formatter = NumberFormatter()
    print(f"Currency: {formatter.format_currency(25.678)}")
    print(f"Percentage: {formatter.format_percentage(0.15)}")
    
    print("\nTesting integrated MathProcessor:")
    processor = MathProcessor()
    result = processor.calculate_tip(50.00, 18)
    
    print(f"Bill: {result['bill']}")
    print(f"Tip ({result['tip_rate']}): {result['tip']}")
    print(f"Total: {result['total']}")