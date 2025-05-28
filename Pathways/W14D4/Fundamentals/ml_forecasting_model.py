# simple_ml_model.py
# Introduction to creating a simple machine learning model for forecasting

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load the data we created in the previous file
try:
    data = pd.read_csv('sales_data.csv')
    print("Data loaded successfully!")
except FileNotFoundError:
    print("Please run basic_data_prep.py first to create the data file.")
    exit()

print("Our data shape:", data.shape)
print(data.head())

# Prepare data for machine learning
# X = features (what we use to predict)
# y = target (what we want to predict)
X = data[['day_number', 'day_of_week']]  # Features
y = data['sales']  # Target (what we want to predict)

print("\nFeatures (X):")
print(X.head())
print("\nTarget (y):")
print(y.head())

# Split data into training and testing sets
# We'll use 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nTraining set size: {len(X_train)} samples")
print(f"Testing set size: {len(X_test)} samples")

# Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

print("\nModel trained successfully!")

# Make predictions on test data
predictions = model.predict(X_test)

print("\nActual vs Predicted sales:")
for i in range(len(y_test)):
    actual = y_test.iloc[i]
    predicted = predictions[i]
    print(f"Day {X_test.iloc[i]['day_number']}: Actual=${actual}, Predicted=${predicted:.2f}")

# Calculate accuracy
mae = mean_absolute_error(y_test, predictions)
print(f"\nModel accuracy (Mean Absolute Error): ${mae:.2f}")
print("This means our predictions are off by about ${:.2f} on average".format(mae))

# Make a future prediction
future_day = 31  # Day 31
future_day_of_week = 1  # Tuesday
future_prediction = model.predict([[future_day, future_day_of_week]])
print(f"\nPrediction for day {future_day} (Tuesday): ${future_prediction[0]:.2f}")