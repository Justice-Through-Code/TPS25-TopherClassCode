# ML Web Application with Flask
# This advanced example shows how to embed ML models in a web application

from flask import Flask, request, render_template_string, jsonify
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import json
import os

# Initialize Flask app
app = Flask(__name__)

# Global variables for model and scaler
model = None
scaler = None
evaluation_results = None

def load_model_and_scaler():
    """Load the trained model and create a scaler for new data"""
    global model, scaler, evaluation_results
    
    try:
        # Load the saved model
        model = joblib.load('best_house_price_model.pkl')
        
        # Load evaluation results
        evaluation_results = np.load('model_evaluation.npy', allow_pickle=True).item()
        
        # Create scaler (in real app, you'd save and load the fitted scaler)
        # For demo, we'll create a new one with known parameters
        scaler = StandardScaler()
        # Set the scaler parameters manually (normally you'd save these)
        scaler.mean_ = np.array([2000, 3, 25])  # Approximate means
        scaler.scale_ = np.array([500, 1.5, 15])  # Approximate scales
        
        print("✅ Model and scaler loaded successfully!")
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Error loading model: {e}")
        print("Please run the basic training scripts first!")
        return False

def preprocess_input(size, bedrooms, age):
    """Preprocess user input to match training data format"""
    # Create feature array
    features = np.array([[size, bedrooms, age]])
    
    # Scale the features
    features_scaled = scaler.transform(features)
    
    return features_scaled

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>House Price Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .input-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 200px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { background: #d4edda; padding: 15px; border-radius: 5px; margin-top: 20px; }
        .error { background: #f8d7da; padding: 15px; border-radius: 5px; margin-top: 20px; }
        .stats { background: #e7f3ff; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🏠 House Price Predictor</h1>
    <p>Enter house details to get an AI-powered price prediction!</p>
    
    <div class="container">
        <form method="POST" action="/predict">
            <div class="input-group">
                <label for="size">House Size (sq ft):</label>
                <input type="number" name="size" id="size" value="2000" min="500" max="5000" required>
            </div>
            
            <div class="input-group">
                <label for="bedrooms">Number of Bedrooms:</label>
                <input type="number" name="bedrooms" id="bedrooms" value="3" min="1" max="10" required>
            </div>
            
            <div class="input-group">
                <label for="age">House Age (years):</label>
                <input type="number" name="age" id="age" value="10" min="0" max="100" required>
            </div>
            
            <button type="submit">🔮 Predict Price</button>
        </form>
    </div>
    
    {% if prediction %}
    <div class="result">
        <h3>💰 Prediction Result</h3>
        <p><strong>Estimated Price: ${{ "%.2f"|format(prediction) }}</strong></p>
        <p><small>Based on house size: {{ size }} sq ft, {{ bedrooms }} bedrooms, {{ age }} years old</small></p>
    </div>
    {% endif %}
    
    {% if error %}
    <div class="error">
        <h3>❌ Error</h3>
        <p>{{ error }}</p>
    </div>
    {% endif %}
    
    <div class="stats">
        <h3>📊 Model Performance</h3>
        {% if model_stats %}
        <p><strong>Model Accuracy (R²):</strong> {{ "%.1f"|format(model_stats.r2 * 100) }}%</p>
        <p><strong>Typical Error (RMSE):</strong> ${{ "%.0f"|format(model_stats.rmse) }}</p>
        <p><strong>Cross-validation Score:</strong> {{ "%.3f"|format(model_stats.cv_mean) }}</p>
        {% else %}
        <p>Model statistics not available</p>
        {% endif %}
    </div>
    
    <div class="container">
        <h3>🤖 About This AI Model</h3>
        <p>This machine learning model was trained on house price data and uses features like size, bedrooms, and age to predict prices. The model has been validated using cross-validation and evaluation metrics.</p>
        <p><strong>Features used:</strong> House size, Number of bedrooms, House age</p>
        <p><strong>Algorithm:</strong> Random Forest Regression</p>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    """Main page with the prediction form"""
    return render_template_string(
        HTML_TEMPLATE, 
        model_stats=evaluation_results if evaluation_results else None
    )

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get form data
        size = float(request.form['size'])
        bedrooms = int(request.form['bedrooms'])
        age = int(request.form['age'])
        
        # Validate input ranges
        if not (500 <= size <= 5000):
            raise ValueError("House size must be between 500 and 5000 sq ft")
        if not (1 <= bedrooms <= 10):
            raise ValueError("Bedrooms must be between 1 and 10")
        if not (0 <= age <= 100):
            raise ValueError("House age must be between 0 and 100 years")
        
        # Preprocess and predict
        features_scaled = preprocess_input(size, bedrooms, age)
        prediction = model.predict(features_scaled)[0]
        
        # Ensure prediction is positive
        prediction = max(prediction, 0)
        
        return render_template_string(
            HTML_TEMPLATE,
            prediction=prediction,
            size=size,
            bedrooms=bedrooms,
            age=age,
            model_stats=evaluation_results
        )
        
    except ValueError as e:
        return render_template_string(
            HTML_TEMPLATE,
            error=str(e),
            model_stats=evaluation_results
        )
    except Exception as e:
        return render_template_string(
            HTML_TEMPLATE,
            error=f"Prediction error: {str(e)}",
            model_stats=evaluation_results
        )

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        
        size = float(data['size'])
        bedrooms = int(data['bedrooms'])
        age = int(data['age'])
        
        # Preprocess and predict
        features_scaled = preprocess_input(size, bedrooms, age)
        prediction = model.predict(features_scaled)[0]
        prediction = max(prediction, 0)
        
        return jsonify({
            'success': True,
            'prediction': float(prediction),
            'input': {
                'size': size,
                'bedrooms': bedrooms,
                'age': age
            },
            'model_performance': evaluation_results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🚀 Starting House Price Prediction Web App...")
    
    # Load model before starting the app
    if load_model_and_scaler():
        print("🌐 Starting web server...")
        print("📱 Open http://127.0.0.1:5000 in your browser")
        print("🔧 API endpoint: POST http://127.0.0.1:5000/api/predict")
        print("❤️  Health check: GET http://127.0.0.1:5000/health")
        
        # Run the Flask app
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("❌ Cannot start app without trained model!")
        print("Please run basic_data_preparation.py and simple_model_training.py first!")