# basic_visualization.py
# Introduction to visualizing forecast data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load and prepare data
try:
    data = pd.read_csv('sales_data.csv')
    print("Data loaded successfully!")
except FileNotFoundError:
    print("Please run basic_data_prep.py first to create the data file.")
    exit()

# Convert date column to datetime
data['date'] = pd.to_datetime(data['date'])

# Prepare and train model (same as before)
X = data[['day_number', 'day_of_week']]
y = data['sales']
model = LinearRegression()
model.fit(X, y)

# Create predictions for existing data
predictions = model.predict(X)

# Create future predictions
future_days = 7  # Predict next 7 days
last_day = data['day_number'].max()
future_dates = pd.date_range(start=data['date'].max() + pd.Timedelta(days=1), 
                           periods=future_days, freq='D')

future_X = []
for i, date in enumerate(future_dates):
    day_num = last_day + i + 1
    day_of_week = date.dayofweek
    future_X.append([day_num, day_of_week])

future_X = np.array(future_X)
future_predictions = model.predict(future_X)

# Create the visualization
plt.figure(figsize=(12, 6))

# Plot historical data
plt.plot(data['date'], data['sales'], 'bo-', label='Actual Sales', markersize=4)

# Plot model predictions for historical data
plt.plot(data['date'], predictions, 'r--', label='Model Fit', alpha=0.7)

# Plot future predictions
plt.plot(future_dates, future_predictions, 'go-', label='Future Predictions', markersize=6)

# Formatting
plt.title('Sales Forecast: Historical Data and Future Predictions', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sales ($)', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()

# Print future predictions
print("\nFuture Predictions:")
for i, (date, pred) in enumerate(zip(future_dates, future_predictions)):
    day_name = date.strftime('%A')
    print(f"{date.strftime('%Y-%m-%d')} ({day_name}): ${pred:.2f}")

# Save the plot
plt.savefig('sales_forecast.png', dpi=300, bbox_inches='tight')
print("\nChart saved as 'sales_forecast.png'")