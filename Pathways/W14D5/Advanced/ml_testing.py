# Advanced ML Testing and Debugging
# This builds on the previous examples with more sophisticated error handling

print("=== Advanced ML Testing and Debugging ===\n")

import random
import json
from datetime import datetime

# Advanced logging for debugging
class MLLogger:
    """Simple logging class for ML debugging"""
    def __init__(self):
        self.logs = []
    
    def log(self, level, message, data=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = {
            "time": timestamp,
            "level": level,
            "message": message,
            "data": data
        }
        self.logs.append(log_entry)
        print(f"[{timestamp}] {level}: {message}")
        if data:
            print(f"  Data: {data}")
    
    def get_logs(self):
        return self.logs

# Create global logger
logger = MLLogger()

# Advanced ML Pipeline with comprehensive error handling
class SimpleMLPipeline:
    """A simple ML pipeline with advanced error handling"""
    
    def __init__(self, name="ML Pipeline"):
        self.name = name
        self.data = None
        self.model_trained = False
        self.weights = None
        logger.log("INFO", f"Initialized {name}")
    
    def load_and_validate_data(self, data_source):
        """Load data with comprehensive validation"""
        try:
            logger.log("INFO", "Starting data loading")
            
            # Simulate different data sources
            if data_source == "database":
                # Simulate database connection issues
                if random.random() < 0.3:  # 30% chance of failure
                    raise ConnectionError("Database connection failed")
                
                self.data = [[random.randint(1, 100), random.randint(1, 100)] 
                           for _ in range(50)]
            
            elif data_source == "file":
                # Simulate file reading
                self.data = [[i, i*2] for i in range(1, 21)]
            
            else:
                raise ValueError(f"Unknown data source: {data_source}")
            
            # Validate loaded data
            self._validate_data()
            logger.log("SUCCESS", f"Loaded {len(self.data)} data points")
            return True
            
        except ConnectionError as e:
            logger.log("ERROR", f"Connection failed: {e}")
            # Fallback to sample data
            self.data = [[1, 2], [3, 4], [5, 6]]
            logger.log("WARNING", "Using fallback sample data")
            return False
            
        except ValueError as e:
            logger.log("ERROR", f"Data validation failed: {e}")
            return False
            
        except Exception as e:
            logger.log("CRITICAL", f"Unexpected error in data loading: {e}")
            return False
    
    def _validate_data(self):
        """Comprehensive data validation"""
        if not self.data:
            raise ValueError("No data loaded")
        
        if len(self.data) < 3:
            logger.log("WARNING", f"Very small dataset: {len(self.data)} points")
        
        # Check for data consistency
        expected_features = len(self.data[0]) if self.data else 0
        for i, row in enumerate(self.data):
            if len(row) != expected_features:
                raise ValueError(f"Inconsistent features at row {i}")
            
            # Check for missing values (None or empty)
            if any(val is None or val == "" for val in row):
                logger.log("WARNING", f"Missing values found at row {i}")
        
        logger.log("INFO", "Data validation passed")
    
    def train_model(self, learning_rate=0.01, max_iterations=100):
        """Train model with parameter validation and monitoring"""
        try:
            logger.log("INFO", "Starting model training")
            
            # Validate training parameters
            if not 0.001 <= learning_rate <= 1.0:
                raise ValueError(f"Learning rate {learning_rate} out of range [0.001, 1.0]")
            
            if not 10 <= max_iterations <= 10000:
                raise ValueError(f"Iterations {max_iterations} out of range [10, 10000]")
            
            if not self.data:
                raise RuntimeError("No data available for training")
            
            # Simulate training process with monitoring
            feature_count = len(self.data[0])
            self.weights = [random.uniform(-1, 1) for _ in range(feature_count)]
            
            # Simulate training iterations with progress monitoring
            for iteration in range(max_iterations):
                # Simulate training step
                if iteration % 20 == 0:  # Log every 20 iterations
                    simulated_loss = 1.0 / (1 + iteration * 0.1)
                    logger.log("DEBUG", f"Iteration {iteration}, Loss: {simulated_loss:.3f}")
                
                # Simulate training instability
                if random.random() < 0.02:  # 2% chance of instability
                    logger.log("WARNING", f"Training instability detected at iteration {iteration}")
                    learning_rate *= 0.9  # Reduce learning rate
            
            self.model_trained = True
            logger.log("SUCCESS", f"Model trained successfully with weights: {[round(w, 3) for w in self.weights]}")
            return True
            
        except ValueError as e:
            logger.log("ERROR", f"Parameter validation failed: {e}")
            return False
            
        except RuntimeError as e:
            logger.log("ERROR", f"Runtime error during training: {e}")
            return False
            
        except Exception as e:
            logger.log("CRITICAL", f"Unexpected training error: {e}")
            return False
    
    def predict_with_confidence(self, input_data, confidence_threshold=0.8):
        """Make predictions with confidence estimation"""
        try:
            if not self.model_trained:
                raise RuntimeError("Model not trained yet")
            
            if not isinstance(input_data, (list, tuple)):
                raise TypeError("Input must be list or tuple")
            
            if len(input_data) != len(self.weights):
                raise ValueError(f"Input size {len(input_data)} doesn't match model {len(self.weights)}")
            
            # Make prediction
            prediction = sum(x * w for x, w in zip(input_data, self.weights))
            
            # Simulate confidence calculation
            confidence = min(0.95, random.uniform(0.6, 1.0))
            
            # Check confidence threshold
            if confidence < confidence_threshold:
                logger.log("WARNING", f"Low confidence prediction: {confidence:.3f}")
                return prediction, confidence, "LOW_CONFIDENCE"
            else:
                logger.log("INFO", f"High confidence prediction: {confidence:.3f}")
                return prediction, confidence, "HIGH_CONFIDENCE"
                
        except RuntimeError as e:
            logger.log("ERROR", f"Prediction failed: {e}")
            return None, 0.0, "ERROR"
            
        except (TypeError, ValueError) as e:
            logger.log("ERROR", f"Input validation failed: {e}")
            return None, 0.0, "INVALID_INPUT"
            
        except Exception as e:
            logger.log("CRITICAL", f"Unexpected prediction error: {e}")
            return None, 0.0, "CRITICAL_ERROR"
    
    def run_comprehensive_test(self):
        """Run a comprehensive test of the pipeline"""
        logger.log("INFO", "Starting comprehensive pipeline test")
        
        # Test 1: Data loading
        success = self.load_and_validate_data("database")
        if not success:
            logger.log("WARNING", "Primary data source failed, trying backup")
            success = self.load_and_validate_data("file")
        
        # Test 2: Model training
        if success:
            success = self.train_model(learning_rate=0.05, max_iterations=80)
        
        # Test 3: Predictions with various inputs
        if success:
            test_inputs = [
                [10, 20],      # Normal case
                [0, 0],        # Edge case: zeros
                [-5, 100],     # Edge case: negative values
                [1000, 2000],  # Edge case: large values
            ]
            
            for i, test_input in enumerate(test_inputs):
                pred, conf, status = self.predict_with_confidence(test_input)
                logger.log("INFO", f"Test {i+1} - Input: {test_input}, Prediction: {pred}, Status: {status}")
        
        logger.log("INFO", "Comprehensive test completed")
        return success

# Example usage
if __name__ == "__main__":
    # Create and test the pipeline
    pipeline = SimpleMLPipeline("Advanced Test Pipeline")
    
    # Run comprehensive test
    success = pipeline.run_comprehensive_test()
    
    print(f"\n=== Test Summary ===")
    print(f"Pipeline test {'PASSED' if success else 'FAILED'}")
    
    # Show all logs
    print(f"\n=== Debug Logs ({len(logger.get_logs())} entries) ===")
    for log in logger.get_logs()[-10:]:  # Show last 10 logs
        print(f"{log['time']} [{log['level']}] {log['message']}")