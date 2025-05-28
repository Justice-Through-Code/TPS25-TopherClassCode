# Complete Testing Framework for ML Applications
# This builds on all previous examples to create a comprehensive testing system

print("=== Complete ML Testing Framework ===\n")

import random
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# Import concepts from previous files
class TestResult:
    """Stores the result of a test case"""
    def __init__(self, name: str, passed: bool, message: str, execution_time: float = 0.0):
        self.name = name
        self.passed = passed
        self.message = message
        self.execution_time = execution_time
        self.timestamp = datetime.now()

class MLTestFramework:
    """Comprehensive testing framework for ML applications"""
    
    def __init__(self, name: str = "ML Test Suite"):
        self.name = name
        self.test_results: List[TestResult] = []
        self.setup_complete = False
        print(f"Initialized {name}")
    
    def setup_test_environment(self):
        """Setup the testing environment with error handling"""
        try:
            print("Setting up test environment...")
            # Simulate environment setup
            time.sleep(0.1)  # Simulate setup time
            
            # Check system requirements
            if not self._check_system_requirements():
                raise RuntimeError("System requirements not met")
            
            self.setup_complete = True
            print("✓ Test environment setup complete")
            return True
            
        except Exception as e:
            print(f"✗ Setup failed: {e}")
            return False
    
    def _check_system_requirements(self):
        """Simulate checking system requirements"""
        # Simulate random system check failure
        return random.random() > 0.1  # 90% success rate
    
    def run_test(self, test_name: str, test_function, *args, **kwargs):
        """Run a single test with comprehensive error handling"""
        if not self.setup_complete:
            print("Warning: Test environment not set up properly")
        
        start_time = time.time()
        
        try:
            print(f"Running test: {test_name}")
            
            # Execute the test function
            result = test_function(*args, **kwargs)
            
            # Determine if test passed
            if isinstance(result, bool):
                passed = result
                message = "Test passed" if passed else "Test failed"
            elif isinstance(result, tuple) and len(result) == 2:
                passed, message = result
            else:
                passed = True
                message = f"Test completed with result: {result}"
            
            execution_time = time.time() - start_time
            
            test_result = TestResult(test_name, passed, message, execution_time)
            self.test_results.append(test_result)
            
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status}: {message} ({execution_time:.3f}s)")
            
            return passed
            
        except AssertionError as e:
            execution_time = time.time() - start_time
            test_result = TestResult(test_name, False, f"Assertion failed: {e}", execution_time)
            self.test_results.append(test_result)
            print(f"  ✗ FAIL: Assertion failed: {e} ({execution_time:.3f}s)")
            return False
            
        except Exception as e:
            execution_time = time.time() - start_time
            test_result = TestResult(test_name, False, f"Exception: {e}", execution_time)
            self.test_results.append(test_result)
            print(f"  ✗ ERROR: {e} ({execution_time:.3f}s)")
            return False
    
    def test_data_validation(self, data: List[List[float]]) -> Tuple[bool, str]:
        """Test data validation with edge cases"""
        # Test 1: Empty data
        if not data:
            return False, "Data is empty"
        
        # Test 2: Minimum size
        if len(data) < 2:
            return False, f"Data too small: {len(data)} rows"
        
        # Test 3: Consistent dimensions
        expected_cols = len(data[0])
        for i, row in enumerate(data):
            if len(row) != expected_cols:
                return False, f"Inconsistent dimensions at row {i}"
        
        # Test 4: Valid values
        for i, row in enumerate(data):
            for j, val in enumerate(row):
                if val is None or (isinstance(val, float) and (val != val)):  # Check for NaN
                    return False, f"Invalid value at row {i}, col {j}"
        
        # Test 5: Reasonable ranges
        flat_values = [val for row in data for val in row]
        if any(abs(val) > 1e6 for val in flat_values):
            return False, "Values outside reasonable range"
        
        return True, f"Data validation passed: {len(data)} rows, {expected_cols} columns"
    
    def test_model_training(self, data: List[List[float]]) -> Tuple[bool, str]:
        """Test model training with various scenarios"""
        try:
            # Simulate model training
            if not data or len(data) < 3:
                return False, "Insufficient data for training"
            
            # Simulate training process
            weights = [random.uniform(-1, 1) for _ in range(len(data[0]))]
            
            # Test for training convergence
            if all(abs(w) < 0.001 for w in weights):
                return False, "Model failed to converge (weights too small)"
            
            # Test for training stability
            if any(abs(w) > 10 for w in weights):
                return False, "Model unstable (weights too large)"
            
            return True, f"Training successful with {len(weights)} weights"
            
        except Exception as e:
            return False, f"Training failed: {e}"
    
    def test_edge_cases(self) -> Tuple[bool, str]:
        """Test various edge cases"""
        edge_cases = [
            ("Empty list", []),
            ("Single item", [[1.0]]),
            ("All zeros", [[0, 0], [0, 0]]),
            ("Large values", [[1e5, 1e5], [1e6, 1e6]]),
            ("Negative values", [[-1, -2], [-3, -4]]),
            ("Mixed signs", [[1, -1], [-1, 1]]),
        ]
        
        failed_cases = []
        
        for case_name, test_data in edge_cases:
            try:
                # Test data validation
                is_valid, msg = self.test_data_validation(test_data)
                
                # Some edge cases are expected to fail validation
                expected_failures = ["Empty list", "Single item"]
                if case_name in expected_failures and not is_valid:
                    continue  # Expected failure
                elif case_name not in expected_failures and not is_valid:
                    failed_cases.append(f"{case_name}: {msg}")
                    
            except Exception as e:
                failed_cases.append(f"{case_name}: Exception {e}")
        
        if failed_cases:
            return False, f"Edge cases failed: {'; '.join(failed_cases)}"
        else:
            return True, f"All {len(edge_cases)} edge cases handled correctly"
    
    def test_prediction_robustness(self, weights: List[float]) -> Tuple[bool, str]:
        """Test prediction function with various inputs"""
        def predict(inputs, weights):
            if len(inputs) != len(weights):
                raise ValueError("Input-weight dimension mismatch")
            return sum(x * w for x, w in zip(inputs, weights))
        
        test_cases = [
            ("Normal case", [1.0, 2.0]),
            ("Zero input", [0.0, 0.0]),
            ("Large input", [1000.0, 2000.0]),
            ("Negative input", [-1.0, -2.0]),
            ("Small decimals", [0.001, 0.002]),
        ]
        
        failed_tests = []
        
        for test_name, test_input in test_cases:
            try:
                result = predict(test_input, weights)
                
                # Check for reasonable output
                if abs(result) > 1e10:
                    failed_tests.append(f"{test_name}: result too large ({result})")
                elif result != result:  # Check for NaN
                    failed_tests.append(f"{test_name}: result is NaN")
                    
            except Exception as e:
                failed_tests.append(f"{test_name}: {e}")
        
        if failed_tests:
            return False, f"Prediction tests failed: {'; '.join(failed_tests)}"
        else:
            return True, f"All {len(test_cases)} prediction tests passed"
    
    def run_comprehensive_test_suite(self):
        """Run the complete test suite"""
        print(f"\n{'='*50}")
        print(f"Running {self.name}")
        print(f"{'='*50}")
        
        # Setup
        if not self.setup_test_environment():
            print("Cannot proceed without proper setup")
            return False
        
        print()
        
        # Generate test data
        test_data = [[random.uniform(0, 100), random.uniform(0, 100)] for _ in range(20)]
        test_weights = [0.5, 0.3]
        
        # Run all tests
        tests = [
            ("Data Validation - Valid Data", self.test_data_validation, test_data),
            ("Data Validation - Empty Data", self.test_data_validation, []),
            ("Data Validation - Inconsistent Data", self.test_data_validation, [[1, 2], [3]]),
            ("Model Training - Normal Case", self.test_model_training, test_data),
            ("Model Training - Insufficient Data", self.test_model_training, [[1, 2]]),
            ("Edge Cases Testing", self.test_edge_cases),
            ("Prediction Robustness", self.test_prediction_robustness, test_weights),
        ]
        
        # Execute all tests
        passed_tests = 0
        for test_args in tests:
            test_name = test_args[0]
            test_func = test_args[1]
            test_params = test_args[2:] if len(test_args) > 2 else []
            
            if self.run_test(test_name, test_func, *test_params):
                passed_tests += 1
        
        # Generate test report
        self.generate_test_report()
        
        # Return overall success
        return passed_tests == len(tests)
    
    def generate_test_report(self):
        """Generate a comprehensive test report"""
        print(f"\n{'='*50}")
        print("TEST REPORT")
        print(f"{'='*50}")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.passed)
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        total_time = sum(result.execution_time for result in self.test_results)
        print(f"Total Execution Time: {total_time:.3f}s")
        
        if failed_tests > 0:
            print(f"\nFAILED TESTS:")
            for result in self.test_results:
                if not result.passed:
                    print(f"  ✗ {result.name}: {result.message}")
        
        print(f"\nDETAILED RESULTS:")
        for result in self.test_results:
            status = "✓" if result.passed else "✗"
            print(f"  {status} {result.name}: {result.message} ({result.execution_time:.3f}s)")

# Advanced test scenarios that combine previous concepts
def test_integration_scenario():
    """Test a complete integration scenario"""
    print("\n=== Integration Test Scenario ===")
    
    # Simulate a complete ML workflow
    try:
        # Step 1: Data loading with error handling
        print("Step 1: Loading data...")
        data = []
        for i in range(15):
            # Simulate some data quality issues
            if i == 5:
                data.append([None, 10])  # Missing value
            elif i == 10:
                data.append([100, float('inf')])  # Invalid value
            else:
                data.append([random.uniform(0, 100), random.uniform(0, 100)])
        
        print(f"  Loaded {len(data)} raw data points")
        
        # Step 2: Data cleaning
        print("Step 2: Cleaning data...")
        clean_data = []
        issues_found = 0
        
        for i, row in enumerate(data):
            # Check for issues
            has_issue = False
            if any(val is None for val in row):
                print(f"  Warning: Missing value at row {i}")
                has_issue = True
                issues_found += 1
            
            if any(isinstance(val, float) and (val == float('inf') or val != val) for val in row):
                print(f"  Warning: Invalid value at row {i}")
                has_issue = True
                issues_found += 1
            
            if not has_issue:
                clean_data.append(row)
        
        print(f"  Cleaned data: {len(clean_data)} points, {issues_found} issues removed")
        
        # Step 3: Model training with monitoring
        print("Step 3: Training model...")
        if len(clean_data) < 5:
            raise ValueError("Insufficient clean data for training")
        
        # Simulate training
        weights = [random.uniform(-1, 1) for _ in range(len(clean_data[0]))]
        print(f"  Model trained with weights: {[round(w, 3) for w in weights]}")
        
        # Step 4: Validation
        print("Step 4: Validating model...")
        test_inputs = [[25, 50], [75, 25], [0, 100]]
        
        for i, test_input in enumerate(test_inputs):
            prediction = sum(x * w for x, w in zip(test_input, weights))
            print(f"  Test {i+1}: {test_input} -> {prediction:.2f}")
        
        print("✓ Integration test PASSED")
        return True
        
    except Exception as e:
        print(f"✗ Integration test FAILED: {e}")
        return False

# Performance testing
def test_performance_scenarios():
    """Test performance under various conditions"""
    print("\n=== Performance Test Scenarios ===")
    
    scenarios = [
        ("Small dataset", 10),
        ("Medium dataset", 100),
        ("Large dataset", 1000),
    ]
    
    for scenario_name, size in scenarios:
        print(f"\nTesting {scenario_name} ({size} points):")
        
        start_time = time.time()
        
        # Generate data
        data = [[random.uniform(0, 100) for _ in range(5)] for _ in range(size)]
        
        # Simulate processing
        processed = 0
        for row in data:
            # Simulate some computation
            result = sum(val * 0.1 for val in row)
            if result > 0:
                processed += 1
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"  Processed {processed}/{size} items in {execution_time:.3f}s")
        print(f"  Rate: {size/execution_time:.1f} items/second")
        
        # Performance thresholds
        if execution_time > 1.0 and size < 1000:
            print(f"  ⚠ Warning: Slow performance for {scenario_name}")
        else:
            print(f"  ✓ Performance acceptable for {scenario_name}")

# Main execution
if __name__ == "__main__":
    # Create and run the comprehensive test framework
    test_framework = MLTestFramework("Advanced ML Testing Suite")
    
    # Run the main test suite
    main_success = test_framework.run_comprehensive_test_suite()
    
    # Run additional integration tests
    integration_success = test_integration_scenario()
    
    # Run performance tests
    test_performance_scenarios()
    
    # Final summary
    print(f"\n{'='*60}")
    print("FINAL TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Main Test Suite: {'PASSED' if main_success else 'FAILED'}")
    print(f"Integration Test: {'PASSED' if integration_success else 'FAILED'}")
    print(f"Overall Status: {'SUCCESS' if main_success and integration_success else 'NEEDS ATTENTION'}")
    
    if not (main_success and integration_success):
        print("\nRecommendations:")
        print("- Review failed test cases in the detailed report above")
        print("- Check data quality and preprocessing steps")
        print("- Validate model parameters and training process")
        print("- Consider edge cases in your ML pipeline")
    else:
        print("\n🎉 All tests passed! Your ML system is robust and well-tested.")