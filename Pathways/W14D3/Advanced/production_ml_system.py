# Production ML System with Model Management
# Advanced example showing model versioning, monitoring, and automated retraining

import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import logging
import sqlite3
import threading
import time
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ml_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ModelManager:
    """Manages ML model lifecycle including versioning and deployment"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = models_dir
        self.current_model = None
        self.current_version = None
        self.model_metadata = {}
        
        # Create models directory
        os.makedirs(models_dir, exist_ok=True)
        
        # Initialize database for tracking
        self.init_database()
        
        logger.info("ModelManager initialized")
    
    def init_database(self):
        """Initialize SQLite database for model tracking"""
        self.conn = sqlite3.connect('ml_system.db', check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS model_versions (
                version TEXT PRIMARY KEY,
                created_at TEXT,
                r2_score REAL,
                rmse REAL,
                training_samples INTEGER,
                status TEXT
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                model_version TEXT,
                input_features TEXT,
                prediction REAL,
                confidence REAL
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS model_performance (
                timestamp TEXT,
                model_version TEXT,
                metric_name TEXT,
                metric_value REAL
            )
        ''')
        
        self.conn.commit()
        logger.info("Database initialized")
    
    def train_new_model(self, X_train: np.ndarray, y_train: np.ndarray, 
                       X_test: np.ndarray, y_test: np.ndarray) -> str:
        """Train a new model version"""
        version = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"Training new model version: {version}")
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=100, 
            random_state=42,
            n_jobs=-1  # Use all CPU cores
        )
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Save model
        model_path = os.path.join(self.models_dir, f"model_{version}.pkl")
        joblib.dump(model, model_path)
        
        # Save metadata
        metadata = {
            'version': version,
            'created_at': datetime.now().isoformat(),
            'r2_score': float(r2),
            'rmse': float(rmse),
            'training_samples': len(X_train),
            'model_path': model_path,
            'status': 'trained'
        }
        
        metadata_path = os.path.join(self.models_dir, f"metadata_{version}.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Store in database
        self.conn.execute('''
            INSERT INTO model_versions 
            (version, created_at, r2_score, rmse, training_samples, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (version, metadata['created_at'], r2, rmse, len(X_train), 'trained'))
        self.conn.commit()
        
        logger.info(f"Model {version} trained - R²: {r2:.3f}, RMSE: {rmse:.2f}")
        return version
    
    def deploy_model(self, version: str) -> bool:
        """Deploy a specific model version"""
        try:
            model_path = os.path.join(self.models_dir, f"model_{version}.pkl")
            metadata_path = os.path.join(self.models_dir, f"metadata_{version}.json")
            
            if not os.path.exists(model_path) or not os.path.exists(metadata_path):
                logger.error(f"Model files not found for version {version}")
                return False
            
            # Load model and metadata
            self.current_model = joblib.load(model_path)
            with open(metadata_path) as f:
                self.model_metadata = json.load(f)
            
            self.current_version = version
            
            # Update database
            self.conn.execute('''
                UPDATE model_versions SET status = 'active' WHERE version = ?
            ''', (version,))
            self.conn.execute('''
                UPDATE model_versions SET status = 'inactive' WHERE version != ?
            ''', (version,))
            self.conn.commit()
            
            logger.info(f"Model {version} deployed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to deploy model {version}: {e}")
            return False
    
    def predict(self, features: np.ndarray, log_prediction: bool = True) -> Dict:
        """Make prediction with current model"""
        if self.current_model is None:
            raise ValueError("No model deployed")
        
        prediction = self.current_model.predict(features)[0]
        
        # Calculate confidence (simplified - based on model's feature importance variance)
        if hasattr(self.current_model, 'feature_importances_'):
            confidence = float(np.mean(self.current_model.feature_importances_))
        else:
            confidence = 0.8  # Default confidence
        
        result = {
            'prediction': float(prediction),
            'confidence': confidence,
            'model_version': self.current_version,
            'timestamp': datetime.now().isoformat()
        }
        
        # Log prediction to database
        if log_prediction:
            self.conn.execute('''
                INSERT INTO predictions 
                (timestamp, model_version, input_features, prediction, confidence)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                result['timestamp'],
                self.current_version,
                json.dumps(features.tolist()),
                prediction,
                confidence
            ))
            self.conn.commit()
        
        return result
    
    def get_model_performance(self, days: int = 7) -> Dict:
        """Get model performance metrics for the last N days"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor = self.conn.execute('''
            SELECT COUNT(*) as prediction_count,
                   AVG(confidence) as avg_confidence,
                   model_version
            FROM predictions 
            WHERE timestamp > ?
            GROUP BY model_version
        ''', (cutoff_date,))
        
        results = cursor.fetchall()
        
        performance = {
            'period_days': days,
            'models': [],
            'total_predictions': 0
        }
        
        for row in results:
            count, avg_conf, version = row
            performance['models'].append({
                'version': version,
                'prediction_count': count,
                'avg_confidence': avg_conf
            })
            performance['total_predictions'] += count
        
        return performance

class MLMonitor:
    """Monitors model performance and triggers retraining when needed"""
    
    def __init__(self, model_manager: ModelManager, check_interval: int = 3600):
        self.model_manager = model_manager
        self.check_interval = check_interval  # seconds
        self.monitoring = False
        self.performance_threshold = 0.7  # R² threshold for retraining
        
    def start_monitoring(self):
        """Start background monitoring"""
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
        logger.info("Model monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.monitoring = False
        logger.info("Model monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                self._check_model_health()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _check_model_health(self):
        """Check if model needs retraining"""
        performance = self.model_manager.get_model_performance(days=1)
        
        if performance['total_predictions'] > 50:  # Only check if we have enough data
            # Check prediction confidence trend
            avg_confidence = np.mean([
                m['avg_confidence'] for m in performance['models']
            ])
            
            if avg_confidence < self.performance_threshold:
                logger.warning(f"Low model confidence detected: {avg_confidence:.3f}")
                # In a real system, this would trigger retraining
                self._log_performance_alert(avg_confidence)
    
    def _log_performance_alert(self, confidence: float):
        """Log performance alert"""
        self.model_manager.conn.execute('''
            INSERT INTO model_performance 
            (timestamp, model_version, metric_name, metric_value)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            self.model_manager.current_version,
            'confidence_alert',
            confidence
        ))
        self.model_manager.conn.commit()

class ProductionMLSystem:
    """Main production ML system class"""
    
    def __init__(self):
        self.model_manager = ModelManager()
        self.monitor = MLMonitor(self.model_manager)
        self.scaler = StandardScaler()
        self.is_initialized = False
        
    def initialize_system(self):
        """Initialize the ML system with training data"""
        logger.info("Initializing production ML system...")
        
        # Generate or load training data
        X_train, X_test, y_train, y_test = self._get_training_data()
        
        # Fit scaler
        self.scaler.fit(X_train)
        
        # Scale data
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train initial model
        version = self.model_manager.train_new_model(
            X_train_scaled, y_train, X_test_scaled, y_test
        )
        
        # Deploy the model
        self.model_manager.deploy_model(version)
        
        # Start monitoring
        self.monitor.start_monitoring()
        
        self.is_initialized = True
        logger.info("Production ML system initialized successfully")
    
    def _get_training_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Generate or load training data"""
        try:
            # Try to load existing data
            X_train = np.load('X_train.npy')
            X_test = np.load('X_test.npy')
            y_train = np.load('y_train.npy')
            y_test = np.load('y_test.npy')
            
            # Convert back to original scale for scaler fitting
            # This is a simplification - in production you'd save the original data
            return X_train * 500 + 2000, X_test * 500 + 2000, y_train, y_test
            
        except FileNotFoundError:
            # Generate synthetic data
            logger.info("Generating synthetic training data")
            np.random.seed(42)
            
            n_samples = 1000
            house_sizes = np.random.normal(2000, 500, n_samples)
            bedrooms = np.random.randint(1, 6, n_samples)
            ages = np.random.randint(1, 50, n_samples)
            
            # More realistic price model
            prices = (
                house_sizes * 100 + 
                bedrooms * 5000 - 
                ages * 200 + 
                np.random.normal(0, 10000, n_samples)
            )
            
            X = np.column_stack([house_sizes, bedrooms, ages])
            y = prices
            
            return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def predict_house_price(self, size: float, bedrooms: int, age: int) -> Dict:
        """Public API for house price prediction"""
        if not self.is_initialized:
            raise RuntimeError("System not initialized. Call initialize_system() first.")
        
        # Prepare features
        features = np.array([[size, bedrooms, age]])
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        result = self.model_manager.predict(features_scaled)
        
        # Add input validation and business logic
        if result['prediction'] < 0:
            result['prediction'] = 50000  # Minimum reasonable price
            result['confidence'] *= 0.5  # Lower confidence for adjusted predictions
        
        # Add human-readable information
        result['input'] = {
            'size': size,
            'bedrooms': bedrooms,
            'age': age
        }
        
        return result
    
    def get_system_status(self) -> Dict:
        """Get overall system status"""
        return {
            'initialized': self.is_initialized,
            'current_model_version': self.model_manager.current_version,
            'model_metadata': self.model_manager.model_metadata,
            'monitoring_active': self.monitor.monitoring,
            'recent_performance': self.model_manager.get_model_performance(days=7),
            'system_uptime': datetime.now().isoformat()
        }
    
    def retrain_model(self) -> str:
        """Manually trigger model retraining"""
        logger.info("Manual model retraining triggered")
        
        # Get fresh training data (in production, this might come from a data pipeline)
        X_train, X_test, y_train, y_test = self._get_training_data()
        
        # Scale data
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train new model
        new_version = self.model_manager.train_new_model(
            X_train_scaled, y_train, X_test_scaled, y_test
        )
        
        # Auto-deploy if better than current model
        if self._should_deploy_new_model(new_version):
            self.model_manager.deploy_model(new_version)
            logger.info(f"New model {new_version} auto-deployed")
        else:
            logger.info(f"New model {new_version} trained but not deployed")
        
        return new_version
    
    def _should_deploy_new_model(self, new_version: str) -> bool:
        """Decide whether to deploy a new model version"""
        if not self.model_manager.current_version:
            return True  # No current model, deploy new one
        
        # Load new model metadata
        new_metadata_path = os.path.join(
            self.model_manager.models_dir, 
            f"metadata_{new_version}.json"
        )
        
        with open(new_metadata_path) as f:
            new_metadata = json.load(f)
        
        # Compare performance
        current_r2 = self.model_manager.model_metadata.get('r2_score', 0)
        new_r2 = new_metadata['r2_score']
        
        # Deploy if new model is significantly better
        improvement_threshold = 0.02  # 2% improvement required
        return new_r2 > current_r2 + improvement_threshold
    
    def shutdown(self):
        """Gracefully shutdown the system"""
        logger.info("Shutting down production ML system...")
        self.monitor.stop_monitoring()
        self.model_manager.conn.close()
        logger.info("System shutdown complete")

# Example usage and demo
def main():
    """Demonstrate the production ML system"""
    print("🚀 Starting Production ML System Demo...")
    
    # Initialize system
    ml_system = ProductionMLSystem()
    ml_system.initialize_system()
    
    # Make some predictions
    print("\n📊 Making sample predictions...")
    
    test_houses = [
        (2500, 3, 5),   # Large, new house
        (1200, 2, 25),  # Small, older house  
        (3000, 4, 2),   # Large, very new house
        (1800, 3, 15),  # Medium house
    ]
    
    for size, bedrooms, age in test_houses:
        result = ml_system.predict_house_price(size, bedrooms, age)
        print(f"🏠 {size} sq ft, {bedrooms} bed, {age} years old:")
        print(f"   💰 Predicted price: ${result['prediction']:,.2f}")
        print(f"   🎯 Confidence: {result['confidence']:.3f}")
        print(f"   📝 Model: {result['model_version']}")
        print()
    
    # Show system status
    print("📈 System Status:")
    status = ml_system.get_system_status()
    print(f"   ✅ Initialized: {status['initialized']}")
    print(f"   🔧 Current model: {status['current_model_version']}")
    print(f"   📊 Model R²: {status['model_metadata']['r2_score']:.3f}")
    print(f"   👁️ Monitoring: {status['monitoring_active']}")
    print(f"   📅 Recent predictions: {status['recent_performance']['total_predictions']}")
    
    # Demonstrate retraining
    print("\n🔄 Demonstrating model retraining...")
    new_version = ml_system.retrain_model()
    print(f"New model version trained: {new_version}")
    
    # Wait a moment to show monitoring
    print("\n⏳ System running... (monitoring active)")
    time.sleep(2)
    
    # Shutdown
    ml_system.shutdown()
    print("✅ Demo complete!")

if __name__ == "__main__":
    main()