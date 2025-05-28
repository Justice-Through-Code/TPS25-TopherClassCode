# Simple ML Integration with Error Handling
# This file shows basic ML operations with safety checks

print("=== Simple ML with Error Handling ===\n")

# We'll simulate simple ML operations without external libraries first
import random

# Example 1: Safe data loading simulation
print("1. Safe Data Loading:")
def load_data(filename):
    """Simulate loading data with error handling"""
    try:
        # Simulate file reading (we'll just create fake data)
        if filename == "bad_file.csv":
            raise FileNotFoundError("File not found")
        
        # Create some fake data
        data = []
        for i in range(10):
            data.append([random.randint(1, 100), random.randint(1, 100)])
        
        print(f"Successfully loaded {len(data)} data points")
        return data
    
    except FileNotFoundError:
        print("Error: Data file not found!")
        print("Using default sample data instead.")
        return [[1, 2], [3, 4], [5, 6]]  # Default small dataset

# Test data loading
good_data = load_data("data.csv")
bad_data = load_data("bad_file.csv")
print(f"Good data sample: {good_data[:3]}")
print(f"Bad data fallback: {bad_data}\n")

# Example 2: Safe prediction function
print("2. Safe Prediction Function:")
def simple_predict(data_point, model_weights):
    """Simple linear prediction with error handling"""
    try:
        # Check if inputs are valid
        if not isinstance(data_point, (list, tuple)):
            raise TypeError("Data point must be a list or tuple")
        
        if len(data_point) != len(model_weights):
            raise ValueError("Data point and weights must have same length")
        
        # Simple prediction: sum of (feature * weight)
        prediction = sum(x * w for x, w in zip(data_point, model_weights))
        return prediction
    
    except TypeError as e:
        print(f"Type Error: {e}")
        return 0
    except ValueError as e:
        print(f"Value Error: {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 0

# Test predictions
weights = [0.5, 0.3]
print(f"Predict [10, 20] = {simple_predict([10, 20], weights)}")
print(f"Predict 'bad input' = {simple_predict('bad input', weights)}")
print(f"Predict [10] (wrong size) = {simple_predict([10], weights)}")
print()

# Example 3: Safe model evaluation
print("3. Safe Model Evaluation:")
def evaluate_model(predictions, actual_values):
    """Calculate accuracy with error handling"""
    try:
        if len(predictions) != len(actual_values):
            raise ValueError("Predictions and actual values must have same length")
        
        if len(predictions) == 0:
            raise ValueError("Cannot evaluate empty predictions")
        
        # Simple accuracy calculation
        correct = sum(1 for p, a in zip(predictions, actual_values) if abs(p - a) < 1)
        accuracy = correct / len(predictions)
        return accuracy
    
    except ValueError as e:
        print(f"Evaluation Error: {e}")
        return 0.0
    except ZeroDivisionError:
        print("Cannot divide by zero in accuracy calculation")
        return 0.0

# Test evaluation
preds = [1.1, 2.2, 3.1]
actual = [1.0, 2.0, 3.0]
empty_preds = []
empty_actual = []

print(f"Normal evaluation: {evaluate_model(preds, actual):.2f}")
print(f"Empty evaluation: {evaluate_model(empty_preds, empty_actual):.2f}")
print(f"Mismatched lengths: {evaluate_model(preds, [1, 2]):.2f}")