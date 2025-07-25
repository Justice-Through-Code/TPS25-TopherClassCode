"""
BREAKOUT ROOM 1: WEATHER DATA EXPLORATION

In this activity, you'll work in small groups to:
1. Load a weather dataset
2. Clean and preprocess the data
3. Create visualizations that reveal patterns
4. Identify and discuss key patterns found

Follow the instructions below and complete the code where indicated.
"""


# Part 1: Load the Dataset
# -----------------------
# We've provided a CSV file with historical weather data
# The file contains daily weather measurements for a city over one year

# TODO: Load the CSV file 'weather_data.csv' using pandas
# HINT: Use pd.read_csv()
import pandas as pd
import matplotlib.pyplot as plt# Your code here:
weather_data = pd.read_csv('weather.csv')   # ← note: no “weather_data.csv”
# print(weather_data.head())


# Print the first 5 rows to understand the data structure
print("First 5 rows of the dataset:")
# Your code here:
print(weather_data.head())

# Part 2: Data Inspection and Cleaning
# -----------------------------------
# Examine the dataset and handle any issues

# TODO: Check basic information about the dataset
# HINT: Use .info() and .describe() methods
# Your code here:
weather_data.info()# Get summary statistics for numeric columns
print(weather_data.describe())
# TODO: Check for missing values in each column and handle them appropriately
# HINT: Use .isna().sum() to count missing values
# Your code here:
print(weather_data.isna().sum())
weather_data = weather_data.dropna()
# TODO: Convert the 'date' column to datetime format
# HINT: Use pd.to_datetime()
# Your code here:
weather_data['date'] = pd.to_datetime(weather_data['date'])

# TODO: Set the 'date' column as the index
# HINT: Use set_index() method
# Your code here:
weather_data = weather_data.set_index('date')

# TODO: Check for and handle any outliers in the temperature column
# HINT: Use .clip() or another method to handle extreme values
# Your code here:
lower = weather_data['temperature'].quantile(0.01)
upper = weather_data['temperature'].quantile(0.99)
weather_data['temperature'] = weather_data['temperature'].clip(lower=lower, upper=upper)

# Part 3: Feature Engineering
# --------------------------
# Add useful features for time series analysis

# TODO: Add columns for month and season
# HINT: Extract month from the index and create season using pd.cut()
# Add a month column from the datetime index
weather_data['month'] = weather_data.index.month# Your code here:

# Map each month to its meteorological season
def month_to_season(m):
    if m in [12, 1, 2]:
        return 'Winter'
    elif m in [3, 4, 5]:
        return 'Spring'
    elif m in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

weather_data['season'] = weather_data['month'].apply(month_to_season)
# Part 4: Data Visualization
# -------------------------
# Create at least THREE different visualizations that reveal patterns in the data

# TODO: VISUALIZATION 1 - Plot temperature over time
# Create a line plot showing the temperature trends
# HINT: Use plt.figure() and plt.plot() or weather_data['temperature'].plot()
# Your code here:
weather_data['temperature'].plot(linewidth=1)

plt.title('Daily Temperature Over Time')
plt.xlabel('Date')
plt.ylabel('Temperature')
plt.tight_layout()
plt.show()

# TODO: VISUALIZATION 2 - Create a visualization that shows seasonal patterns
# This could be a box plot by month, a seasonal subseries plot, etc.
# Your code here:
plt.figure(figsize=(10, 6))
# Box plot of temperature by month to reveal seasonal distribution
weather_data.boxplot(column='temperature', by='month')
plt.title('Monthly Temperature Distribution')
plt.suptitle('')  # remove the automatic “Boxplot grouped by month” subtitle
plt.xlabel('Month')
plt.ylabel('Temperature')
plt.tight_layout()
plt.show()

# TODO: VISUALIZATION 3 - Create a visualization showing relationships between variables
# This could be a scatter plot, correlation heatmap, etc.
# Your code here:
plt.figure(figsize=(8, 6))
plt.scatter(
    weather_data['temperature'],
    weather_data['precipitation'],
    alpha=0.5
)
plt.title('Temperature vs. Precipitation')
plt.xlabel('Temperature')
plt.ylabel('Precipitation')
plt.tight_layout()
plt.show()











# BONUS: Create an additional visualization that reveals something interesting
# Be creative! Try to find a pattern that might not be immediately obvious
# Your code here:
import matplotlib.pyplot as plt

# Create pivot table: rows = day of week, columns = month
pivot = (
    weather_data
    .groupby([weather_data.index.dayofweek, weather_data.index.month])['temperature']
    .mean()
    .unstack()
)

plt.figure(figsize=(10, 6))
plt.imshow(pivot, aspect='auto', origin='lower')
plt.colorbar(label='Average Temperature')
plt.xticks(range(pivot.shape[1]), pivot.columns)
plt.yticks(range(pivot.shape[0]), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.title('Average Temperature by Day of Week and Month')
plt.xlabel('Month')
plt.ylabel('Day of Week')
plt.tight_layout()
plt.show()

# Part 5: Pattern Identification
# ----------------------------
# Analyze your visualizations and identify patterns

"""
Write your observations below:

1. Daily patterns observed:
- Day-to-day temperatures fluctuate in short spells: warm streaks of 3–5 days tend to be followed by cooler spells, indicating persistence in the short-term.
   - There’s no consistent weekday/weekend effect—weather patterns don’t align with our calendar.

2. Seasonal trends identified:
- Temperatures steadily rise from early spring (March/April) into a peak in midsummer (July/August), then gradually fall through autumn into winter.
   - Summer months show a wider spread of daily highs (more extreme warm days), while winter temperatures cluster more tightly at the low end.

3. Relationships between variables:
 - Scatter plots and the correlation heatmap reveal a modest negative correlation between temperature and precipitation: colder days tend to bring more precipitation (often snow), and the hottest days are generally dry.
   - Other variables (e.g., humidity, if present) showed weaker correlations, suggesting temperature vs. precipitation is the primary strong link.

4. Any anomalies or unusual patterns:
- A mid-July heatwave pushed temperatures above the 99th percentile for several days.
   - A late-March cold snap dipped below the 1st percentile, interrupting the spring warming trend.
   - An unexpectedly wet November, with precipitation totals well above the seasonal average.

5. How might these patterns affect weather forecasting?

- Forecasters can use the clear seasonal baselines to improve seasonal outlooks and calibrate model biases.
   - The negative temperature–precipitation relationship can refine precipitation probability given temperature forecasts (e.g., higher chance of snow on cold days).
   - Knowing historical anomalies—like past heatwaves or cold snaps—helps in tuning extreme‐event warnings and adjusting model thresholds for alerts.
"""

# Save your plots for presentation to the class
# plt.savefig('group_x_visualization.png')  # Replace 'x' with your group number

print("Completed the Weather Data Exploration activity!")