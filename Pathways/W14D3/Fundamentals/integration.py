# simple_ml_app.py
from sklearn.linear_model import LinearRegression
import numpy as np

# Train a simple model
def train_model():
    # Data: hours studied -> test score
    hours = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
    scores = np.array([50, 55, 65, 70, 80, 85, 90, 95])
    
    model = LinearRegression()
    model.fit(hours, scores)
    return model

# Use the model
def predict_score(model, hours_studied):
    return model.predict([[hours_studied]])[0]

# Simple app
if __name__ == "__main__":
    print("=== Study Score Predictor ===")
    
    # Train the model once
    model = train_model()
    print("Model trained!")
    
    # Use the model
    while True:
        try:
            hours = float(input("\nHours studied (or 0 to quit): "))
            if hours == 0:
                break
            
            score = predict_score(model, hours)
            print(f"Predicted test score: {score:.1f}")
            
        except ValueError:
            print("Please enter a valid number")
    
    print("Goodbye!")