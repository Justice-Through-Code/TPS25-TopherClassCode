# Model Evaluation and Validation
# This file demonstrates how to properly evaluate ML models

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score, validation_curve
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

print("=== Loading Model and Data ===")
try:
    # Load saved model
    model = joblib.load('best_house_price_model.pkl')
    
    # Load test data
    X_test = np.load('X_test.npy')
    y_test = np.load('y_test.npy')
    X_train = np.load('X_train.npy')
    y_train = np.load('y_train.npy')
    
    print("Model and data loaded successfully!")
except FileNotFoundError:
    print("Error: Please run the previous scripts first!")
    exit()

# Make predictions on test set
print("\n=== Making Predictions ===")
y_pred = model.predict(X_test)

# Calculate multiple evaluation metrics
print("\n=== Detailed Model Evaluation ===")
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): ${mae:,.2f}")
print(f"Mean Squared Error (MSE): {mse:,.2f}")
print(f"Root Mean Squared Error (RMSE): ${rmse:,.2f}")
print(f"R² Score: {r2:.3f}")

# Explain what these metrics mean
print("\n=== What These Metrics Mean ===")
print(f"• MAE: On average, predictions are off by ${mae:,.0f}")
print(f"• RMSE: Emphasizes larger errors, typical error is ${rmse:,.0f}")
print(f"• R²: Model explains {r2*100:.1f}% of the price variation")

# Cross-validation for more robust evaluation
print("\n=== Cross-Validation ===")
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
print(f"Cross-validation R² scores: {cv_scores}")
print(f"Mean CV R²: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")

# Check for overfitting
print("\n=== Overfitting Check ===")
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training R²: {train_score:.3f}")
print(f"Testing R²: {test_score:.3f}")
print(f"Difference: {train_score - test_score:.3f}")

if train_score - test_score > 0.1:
    print("⚠️  Possible overfitting detected!")
else:
    print("✅ Model generalizes well!")

# Residual analysis (prediction errors)
print("\n=== Residual Analysis ===")
residuals = y_test - y_pred
mean_residual = np.mean(residuals)
std_residual = np.std(residuals)

print(f"Mean residual: ${mean_residual:.2f}")
print(f"Std deviation of residuals: ${std_residual:.2f}")

# Check if residuals are normally distributed (good sign)
print(f"Residuals range: ${residuals.min():.0f} to ${residuals.max():.0f}")

# Simple visualization (text-based)
print("\n=== Prediction vs Actual (Sample) ===")
print("Actual Price    | Predicted Price | Error")
print("-" * 45)
for i in range(min(10, len(y_test))):
    error = abs(y_test[i] - y_pred[i])
    print(f"${y_test[i]:>10,.0f} | ${y_pred[i]:>13,.0f} | ${error:>8,.0f}")

# Model performance summary
print("\n=== Model Performance Summary ===")
if r2 > 0.8:
    performance = "Excellent"
elif r2 > 0.6:
    performance = "Good"
elif r2 > 0.4:
    performance = "Fair"
else:
    performance = "Poor"

print(f"Overall Performance: {performance}")
print(f"Model explains {r2*100:.1f}% of house price variation")
print(f"Typical prediction error: ${rmse:,.0f}")

# Save evaluation results
print("\n=== Saving Evaluation Results ===")
evaluation_results = {
    'mae': mae,
    'mse': mse,
    'rmse': rmse,
    'r2': r2,
    'cv_mean': cv_scores.mean(),
    'cv_std': cv_scores.std(),
    'train_score': train_score,
    'test_score': test_score
}

# Save as numpy file for use in applications
np.save('model_evaluation.npy', evaluation_results)
print("Evaluation results saved!")