import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Generate simple data points
hours_studied = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
exam_scores= np.array([50, 55, 65, 70, 80, 85, 90, 95])

# Create machine learning model
model = LinearRegression()
model.fit(hours_studied, exam_scores)

# Predict potential future scores
prediction_hours = np.array(range(1, 10)).reshape(-1, 1)
predicted_scores = model.predict(prediction_hours)

# Create visualization
plt.figure(figsize=(10, 6))
plt.scatter(hours_studied, exam_scores, color='blue', label='Actual Data')
plt.plot(prediction_hours, predicted_scores, color='red', label='Prediction')
plt.title('Study Hours vs Exam Scores')
plt.xlabel('Hours Studied')
plt.ylabel('Exam Score')
plt.legend()
plt.grid(True)
plt.show()