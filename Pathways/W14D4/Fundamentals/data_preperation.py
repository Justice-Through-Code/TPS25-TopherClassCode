# basic_data_prep.py
# Introduction to preparing data for machine learning forecasting

import pandas as pd
import numpy as np

# Create sample sales data (like a small business tracking daily sales)
dates = pd.date_range('2024-01-01', periods=30, freq='D')
sales = [100, 120, 95, 130, 110, 140, 125, 160, 145, 170,
         155, 180, 165, 190, 175, 200, 185, 210, 195, 220,
         205, 230, 215, 240, 225, 250, 235, 260, 245, 270]

# Create a DataFrame (like a spreadsheet in Python)
data = pd.DataFrame({
    'date': dates,
    'sales': sales
})

print("Our sample data:")
print(data.head(10))  # Show first 10 rows

# Add some basic features that might help with forecasting
data['day_of_week'] = data['date'].dt.dayofweek  # 0=Monday, 6=Sunday
data['day_number'] = range(1, len(data) + 1)  # Sequential day number

print("\nData with additional features:")
print(data.head())

# Save the data for use in other files
data.to_csv('sales_data.csv', index=False)
print("\nData saved to 'sales_data.csv'")

# Basic statistics
print(f"\nBasic Statistics:")
print(f"Average daily sales: ${data['sales'].mean():.2f}")
print(f"Highest sales day: ${data['sales'].max()}")
print(f"Lowest sales day: ${data['sales'].min()}")