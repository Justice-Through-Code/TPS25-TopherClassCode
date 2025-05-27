# Simple Model Training Example
# This file shows how to train a basic machine learning model

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

print("=== Loading Prepared Data ===")
# Load the data we prepared in the previous file
try:
    X_train = np.load('X_train.npy')
    X_test = np.load('X_test.npy')
    y_train = np.load('y_train.npy')
    y_test = np.load('y_test.npy')
    print("Data loaded successfully!")
except FileNotFoundError:
    print("Error: Please run basic_data_preparation.py first!")
    exit()

print(f"Training data shape: {X_train.shape}")
print(f"Test data shape: {X_test.shape}")

# Train a Linear Regression model
print("\n=== Training Linear Regression Model ===")
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Make predictions
linear_predictions = linear_model.predict(X_test)

# Evaluate the model
linear_mse = mean_squared_error(y_test, linear_predictions)
linear_r2 = r2_score(y_test, linear_predictions)

print(f"Linear Regression Results:")
print(f"  Mean Squared Error: {linear_mse:.2f}")
print(f"  R² Score: {linear_r2:.3f}")

# Train a Random Forest model (more complex)
print("\n=== Training Random Forest Model ===")
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions
rf_predictions = rf_model.predict(X_test)

# Evaluate the model
rf_mse = mean_squared_error(y_test, rf_predictions)
rf_r2 = r2_score(y_test, rf_predictions)

print(f"Random Forest Results:")
print(f"  Mean Squared Error: {rf_mse:.2f}")
print(f"  R² Score: {rf_r2:.3f}")

# Compare models
print("\n=== Model Comparison ===")
if rf_r2 > linear_r2:
    best_model = rf_model
    best_name = "Random Forest"
    print(f"Random Forest performs better (R² = {rf_r2:.3f})")
else:
    best_model = linear_model
    best_name = "Linear Regression"
    print(f"Linear Regression performs better (R² = {linear_r2:.3f})")

# Save the best model
print(f"\n=== Saving Best Model ({best_name}) ===")
joblib.dump(best_model, 'best_house_price_model.pkl')
print("Model saved as 'best_house_price_model.pkl'")

# Show feature importance (if Random Forest won)
if best_name == "Random Forest":
    print("\n=== Feature Importance ===")
    feature_names = ['House Size', 'Bedrooms', 'Age']
    importances = best_model.feature_importances_
    
    for name, importance in zip(feature_names, importances):
        print(f"  {name}: {importance:.3f}")

# Make a sample prediction
print("\n=== Sample Prediction ===")
# Predict price for a house: 2500 sq ft, 3 bedrooms, 10 years old
# Note: This should be scaled the same way as training data
sample_house = np.array([[0.5, 0.2, -0.8]])  # Pre-scaled values for example
predicted_price = best_model.predict(sample_house)
print(f"Predicted price for sample house: ${predicted_price[0]:,.2f}")

print("\nModel training complete!")