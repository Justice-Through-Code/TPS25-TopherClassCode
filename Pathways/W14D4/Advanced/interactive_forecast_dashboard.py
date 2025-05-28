# advanced_forecast_dashboard.py
# Advanced interactive dashboard for forecast visualization
# Builds on previous files to create a more sophisticated interface

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class ForecastDashboard:
    def __init__(self):
        self.data = None
        self.models = {}
        self.predictions = {}
        self.future_predictions = {}
        
    def load_data(self, filename='sales_data.csv'):
        """Load and prepare data for forecasting"""
        try:
            self.data = pd.read_csv(filename)
            self.data['date'] = pd.to_datetime(self.data['date'])
            print(f"✓ Data loaded: {len(self.data)} records")
            return True
        except FileNotFoundError:
            print("❌ Data file not found. Please run basic_data_prep.py first.")
            return False
    
    def train_models(self):
        """Train multiple ML models for comparison"""
        if self.data is None:
            print("❌ No data loaded!")
            return
        
        # Prepare features
        X = self.data[['day_number', 'day_of_week']]
        y = self.data['sales']
        
        # Train different models
        models_to_train = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        for name, model in models_to_train.items():
            model.fit(X, y)
            predictions = model.predict(X)
            mae = mean_absolute_error(y, predictions)
            
            self.models[name] = model
            self.predictions[name] = predictions
            
            print(f"✓ {name} trained - MAE: ${mae:.2f}")
    
    def generate_future_forecasts(self, days_ahead=14):
        """Generate future predictions with multiple models"""
        if not self.models:
            print("❌ No models trained!")
            return
        
        # Create future dates and features
        last_day = self.data['day_number'].max()
        last_date = self.data['date'].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), 
                                   periods=days_ahead, freq='D')
        
        # Prepare future features
        future_X = []
        for i, date in enumerate(future_dates):
            day_num = last_day + i + 1
            day_of_week = date.dayofweek
            future_X.append([day_num, day_of_week])
        
        future_X = np.array(future_X)
        
        # Generate predictions for each model
        future_df = pd.DataFrame({'date': future_dates})
        
        for name, model in self.models.items():
            predictions = model.predict(future_X)
            future_df[f'{name}_prediction'] = predictions
            self.future_predictions[name] = predictions
        
        self.future_df = future_df
        print(f"✓ Generated {days_ahead} days of forecasts")
    
    def create_comprehensive_dashboard(self):
        """Create a comprehensive visualization dashboard"""
        if self.data is None or not self.models:
            print("❌ Data or models not ready!")
            return
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Advanced Sales Forecasting Dashboard', fontsize=16, fontweight='bold')
        
        # Plot 1: Historical data with model comparisons
        ax1 = axes[0, 0]
        ax1.plot(self.data['date'], self.data['sales'], 'ko-', 
                label='Actual Sales', markersize=3, linewidth=2)
        
        colors = ['red', 'blue', 'green', 'orange']
        for i, (name, pred) in enumerate(self.predictions.items()):
            ax1.plot(self.data['date'], pred, '--', 
                    color=colors[i], label=f'{name} Fit', alpha=0.7)
        
        ax1.set_title('Historical Data & Model Fits')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Sales ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Future predictions comparison
        ax2 = axes[0, 1]
        # Show last 10 days of historical data for context
        recent_data = self.data.tail(10)
        ax2.plot(recent_data['date'], recent_data['sales'], 'ko-', 
                label='Recent Actual', markersize=4)
        
        for i, (name, pred) in enumerate(self.future_predictions.items()):
            ax2.plot(self.future_df['date'], pred, 'o-', 
                    color=colors[i], label=f'{name} Forecast', markersize=3)
        
        ax2.set_title('Future Forecasts Comparison')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Sales ($)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Sales by day of week
        ax3 = axes[1, 0]
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        daily_avg = self.data.groupby('day_of_week')['sales'].mean()
        bars = ax3.bar(range(7), daily_avg.values, color='skyblue', alpha=0.7)
        ax3.set_title('Average Sales by Day of Week')
        ax3.set_xlabel('Day of Week')
        ax3.set_ylabel('Average Sales ($)')
        ax3.set_xticks(range(7))
        ax3.set_xticklabels(day_names)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'${height:.0f}', ha='center', va='bottom')
        
        # Plot 4: Model performance comparison
        ax4 = axes[1, 1]
        model_names = list(self.models.keys())
        mae_scores = []
        rmse_scores = []
        
        for name in model_names:
            mae = mean_absolute_error(self.data['sales'], self.predictions[name])
            rmse = np.sqrt(mean_squared_error(self.data['sales'], self.predictions[name]))
            mae_scores.append(mae)
            rmse_scores.append(rmse)
        
        x = np.arange(len(model_names))
        width = 0.35
        
        bars1 = ax4.bar(x - width/2, mae_scores, width, label='MAE', alpha=0.7)
        bars2 = ax4.bar(x + width/2, rmse_scores, width, label='RMSE', alpha=0.7)
        
        ax4.set_title('Model Performance Comparison')
        ax4.set_xlabel('Models')
        ax4.set_ylabel('Error ($)')
        ax4.set_xticks(x)
        ax4.set_xticklabels(model_names)
        ax4.legend()
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'${height:.1f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.show()
        
        # Save the dashboard
        plt.savefig('advanced_forecast_dashboard.png', dpi=300, bbox_inches='tight')
        print("✓ Dashboard saved as 'advanced_forecast_dashboard.png'")
    
    def print_forecast_summary(self):
        """Print a detailed forecast summary"""
        if not hasattr(self, 'future_df'):
            print("❌ No future forecasts generated!")
            return
        
        print("\n" + "="*60)
        print("FORECAST SUMMARY")
        print("="*60)
        
        for _, row in self.future_df.iterrows():
            date_str = row['date'].strftime('%Y-%m-%d (%A)')
            print(f"\n{date_str}:")
            
            for name in self.models.keys():
                pred_col = f'{name}_prediction'
                print(f"  {name}: ${row[pred_col]:.2f}")
        
        # Weekly summary
        if len(self.future_df) >= 7:
            print(f"\n" + "-"*40)
            print("WEEKLY FORECAST SUMMARY")
            print("-"*40)
            
            for name in self.models.keys():
                pred_col = f'{name}_prediction'
                weekly_total = self.future_df[pred_col].head(7).sum()
                weekly_avg = self.future_df[pred_col].head(7).mean()
                print(f"{name}:")
                print(f"  Total week sales: ${weekly_total:.2f}")
                print(f"  Average daily sales: ${weekly_avg:.2f}")

# Main execution
if __name__ == "__main__":
    print("🚀 Starting Advanced Forecast Dashboard...")
    
    # Create dashboard instance
    dashboard = ForecastDashboard()
    
    # Load data
    if dashboard.load_data():
        # Train models
        dashboard.train_models()
        
        # Generate forecasts
        dashboard.generate_future_forecasts(days_ahead=14)
        
        # Create visualizations
        dashboard.create_comprehensive_dashboard()
        
        # Print summary
        dashboard.print_forecast_summary()
        
        print("\n✅ Advanced dashboard complete!")
    else:
        print("❌ Dashboard creation failed. Please check data file.")