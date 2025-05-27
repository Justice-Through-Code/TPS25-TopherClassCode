# Basic Data Preparation for Machine Learning
# This file demonstrates how to prepare data for ML models

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Create sample data (simulating house prices)
print("=== Creating Sample Data ===")
np.random.seed(42)  # For reproducible results

# Generate fake house data
house_sizes = np.random.normal(2000, 500, 100)  # Square feet
bedrooms = np.random.randint(1, 6, 100)
ages = np.random.randint(1, 50, 100)

# Create prices with some realistic relationship
prices = (house_sizes * 100) + (bedrooms * 5000) - (ages * 200) + np.random.normal(0, 10000, 100)

# Create DataFrame
data = pd.DataFrame({
    'size': house_sizes,
    'bedrooms': bedrooms,
    'age': ages,
    'price': prices
})

print("First 5 rows of our data:")
print(data.head())
print(f"\nDataset shape: {data.shape}")

# Basic data exploration
print("\n=== Data Exploration ===")
print("Data types:")
print(data.dtypes)
print("\nBasic statistics:")
print(data.describe())

# Check for missing values
print(f"\nMissing values: {data.isnull().sum().sum()}")

# Prepare features (X) and target (y)
print("\n=== Preparing Features and Target ===")
X = data[['size', 'bedrooms', 'age']]  # Features
y = data['price']  # Target variable

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")

# Split data into training and testing sets
print("\n=== Splitting Data ===")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

# Scale the features (important for many ML algorithms)
print("\n=== Scaling Features ===")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Features scaled successfully!")
print(f"Original feature means: {X_train.mean().values}")
print(f"Scaled feature means: {X_train_scaled.mean(axis=0)}")

# Save prepared data for next examples
print("\n=== Saving Prepared Data ===")
np.save('X_train.npy', X_train_scaled)
np.save('X_test.npy', X_test_scaled)
np.save('y_train.npy', y_train.values)
np.save('y_test.npy', y_test.values)

print("Data preparation complete! Files saved for training.")