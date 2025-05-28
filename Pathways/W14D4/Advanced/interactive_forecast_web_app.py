# interactive_forecast_app.py
# Interactive web application for forecast visualization
# Combines all previous concepts into a user-friendly web interface

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import datetime
import warnings
warnings.filterwarnings('ignore')

# Streamlit page configuration
st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📈",
    layout="wide"
)

class InteractiveForecastApp:
    def __init__(self):
        self.data = None
        self.models = {}
        
    @st.cache_data
    def load_sample_data(_self):
        """Create or load sample data"""
        # Try to load existing data first
        try:
            data = pd.read_csv('sales_data.csv')
            data['date'] = pd.to_datetime(data['date'])
        except FileNotFoundError:
            # Create sample data if file doesn't exist
            st.info("Creating sample data...")
            dates = pd.date_range('2024-01-01', periods=60, freq='D')
            
            # Create more realistic sales data with trends and seasonality
            trend = np.linspace(100, 300, 60)
            seasonality = 20 * np.sin(np.linspace(0, 4*np.pi, 60))
            weekly_pattern = np.tile([1.2, 1.1, 1.0, 1.0, 1.3, 1.5, 1.4], 9)[:60]
            noise = np.random.normal(0, 10, 60)
            
            sales = (trend + seasonality) * weekly_pattern + noise
            sales = np.maximum(sales, 50)  # Ensure positive sales
            
            data = pd.DataFrame({
                'date': dates,
                'sales': sales.round(2)
            })
            
            data['day_of_week'] = data['date'].dt.dayofweek
            data['day_number'] = range(1, len(data) + 1)
            
        _self.data = data
        return data
    
    def train_models(self, data):
        """Train multiple forecasting models"""
        X = data[['day_number', 'day_of_week']]
        y = data['sales']
        
        models = {
            'Linear Regression': LinearRegression(),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        trained_models = {}
        model_scores = {}
        
        for name, model in models.items():
            model.fit(X, y)
            predictions = model.predict(X)
            mae = mean_absolute_error(y, predictions)
            
            trained_models[name] = model
            model_scores[name] = mae
        
        return trained_models, model_scores
    
    def generate_forecasts(self, models, data, days_ahead):
        """Generate future forecasts"""
        last_day = data['day_number'].max()
        last_date = data['date'].max()
        
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1), 
            periods=days_ahead, 
            freq='D'
        )
        
        future_X = []
        for i, date in enumerate(future_dates):
            day_num = last_day + i + 1
            day_of_week = date.dayofweek
            future_X.append([day_num, day_of_week])
        
        future_X = np.array(future_X)
        
        forecasts = {'date': future_dates}
        for name, model in models.items():
            forecasts[name] = model.predict(future_X)
        
        return pd.DataFrame(forecasts)
    
    def create_main_chart(self, historical_data, forecast_data, selected_models):
        """Create the main interactive forecast chart"""
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['sales'],
            mode='lines+markers',
            name='Historical Sales',
            line=dict(color='blue', width=3),
            marker=dict(size=6)
        ))
        
        # Forecast data for selected models
        colors = ['red', 'green', 'orange', 'purple']
        for i, model in enumerate(selected_models):
            if model in forecast_data.columns:
                fig.add_trace(go.Scatter(
                    x=forecast_data['date'],
                    y=forecast_data[model],
                    mode='lines+markers',
                    name=f'{model} Forecast',
                    line=dict(color=colors[i % len(colors)], width=2, dash='dash'),
                    marker=dict(size=8)
                ))
        
        fig.update_layout(
            title="Sales Forecast Dashboard",
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            hovermode='x unified',
            height=500
        )
        
        return fig
    
    def create_performance_chart(self, model_scores):
        """Create model performance comparison chart"""
        models = list(model_scores.keys())
        scores = list(model_scores.values())
        
        fig = go.Figure(data=[
            go.Bar(x=models, y=scores, text=[f'${s:.2f}' for s in scores],
                   textposition='auto')
        ])
        
        fig.update_layout(
            title="Model Performance Comparison (Lower is Better)",
            yaxis_title="Mean Absolute Error ($)",
            height=400
        )
        
        return fig
    
    def create_daily_pattern_chart(self, data):
        """Create daily pattern analysis chart"""
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                    'Friday', 'Saturday', 'Sunday']
        
        daily_avg = data.groupby('day_of_week')['sales'].agg(['mean', 'std']).reset_index()
        daily_avg['day_name'] = [day_names[i] for i in daily_avg['day_of_week']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=daily_avg['day_name'],
            y=daily_avg['mean'],
            error_y=dict(type='data', array=daily_avg['std']),
            name='Average Sales',
            text=[f'${x:.0f}' for x in daily_avg['mean']],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Average Sales by Day of Week",
            xaxis_title="Day of Week",
            yaxis_title="Average Sales ($)",
            height=400
        )
        
        return fig

def main():
    st.title("📈 Interactive Sales Forecasting Dashboard")
    st.markdown("*Built on machine learning models for business forecasting*")
    
    # Initialize app
    app = InteractiveForecastApp()
    
    # Sidebar controls
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Load data
    with st.spinner("Loading data..."):
        data = app.load_sample_data()
    
    st.sidebar.success(f"✅ Data loaded: {len(data)} records")
    
    # Forecast parameters
    st.sidebar.subheader("Forecast Settings")
    days_ahead = st.sidebar.slider("Days to forecast", 1, 30, 14)
    
    # Model selection
    available_models = ['Linear Regression', 'Random Forest']
    selected_models = st.sidebar.multiselect(
        "Select models to display",
        available_models,
        default=available_models
    )
    
    # Train models
    with st.spinner("Training models..."):
        models, model_scores = app.train_models(data)
    
    # Generate forecasts
    with st.spinner("Generating forecasts..."):
        forecasts = app.generate_forecasts(models, data, days_ahead)
    
    # Main dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Historical Sales", f"${data['sales'].sum():,.2f}")
    
    with col2:
        avg_daily = data['sales'].mean()
        st.metric("Average Daily Sales", f"${avg_daily:.2f}")
    
    with col3:
        if selected_models:
            best_model = min(model_scores.keys(), key=lambda x: model_scores[x])
            st.metric("Best Model", best_model, f"MAE: ${model_scores[best_model]:.2f}")
    
    # Main forecast chart
    st.subheader("📊 Sales Forecast")
    if selected_models:
        main_chart = app.create_main_chart(data, forecasts, selected_models)
        st.plotly_chart(main_chart, use_container_width=True)
    else:
        st.warning("Please select at least one model to display forecasts.")
    
    # Additional charts in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Model Performance")
        perf_chart = app.create_performance_chart(model_scores)
        st.plotly_chart(perf_chart, use_container_width=True)
    
    with col2:
        st.subheader("📅 Daily Patterns")
        pattern_chart = app.create_daily_pattern_chart(data)
        st.plotly_chart(pattern_chart, use_container_width=True)
    
    # Forecast table
    st.subheader("📋 Detailed Forecast")
    if selected_models:
        display_forecasts = forecasts[['date'] + selected_models].copy()
        display_forecasts['date'] = display_forecasts['date'].dt.strftime('%Y-%m-%d (%A)')
        
        # Format currency columns
        for model in selected_models:
            display_forecasts[model] = display_forecasts[model].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_forecasts, use_container_width=True)
        
        # Summary statistics
        st.subheader("📈 Forecast Summary")
        summary_cols = st.columns(len(selected_models))
        
        for i, model in enumerate(selected_models):
            with summary_cols[i]:
                total_forecast = forecasts[model].sum()
                avg_forecast = forecasts[model].mean()
                st.metric(
                    f"{model}",
                    f"${total_forecast:.2f}",
                    f"Avg: ${avg_forecast:.2f}"
                )
    
    # Data insights
    with st.expander("🔍 Data Insights"):
        st.write("**Key Insights from the Data:**")
        
        # Growth trend
        recent_avg = data['sales'].tail(7).mean()
        early_avg = data['sales'].head(7).mean()
        growth_rate = ((recent_avg - early_avg) / early_avg) * 100
        
        st.write(f"• **Growth Trend**: {growth_rate:+.1f}% change from early to recent period")
        
        # Best day
        best_day_idx = data.groupby('day_of_week')['sales'].mean().idxmax()
        best_day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                        'Friday', 'Saturday', 'Sunday'][best_day_idx]
        best_day_sales = data.groupby('day_of_week')['sales'].mean().max()
        
        st.write(f"• **Best Sales Day**: {best_day_name} (avg: ${best_day_sales:.2f})")
        
        # Volatility
        volatility = data['sales'].std()
        st.write(f"• **Sales Volatility**: ${volatility:.2f} standard deviation")
        
        # Model recommendations
        best_model = min(model_scores.keys(), key=lambda x: model_scores[x])
        st.write(f"• **Recommended Model**: {best_model} (lowest error rate)")
    
    # Footer
    st.markdown("---")
    st.markdown("**How to use this dashboard:**")
    st.markdown("""
    1. **Adjust forecast period** using the slider in the sidebar
    2. **Select models** to compare different forecasting approaches
    3. **Analyze patterns** in the daily sales chart
    4. **Review detailed forecasts** in the table below
    5. **Use insights** to make informed business decisions
    """)
    
    # Technical notes
    with st.expander("🔧 Technical Details"):
        st.markdown("""
        **Models Used:**
        - **Linear Regression**: Simple trend-based forecasting
        - **Random Forest**: Advanced ensemble method for complex patterns
        
        **Features:**
        - Day number (sequential timeline)
        - Day of week (weekly seasonality)
        
        **Metrics:**
        - MAE (Mean Absolute Error): Average prediction error in dollars
        
        **Data Processing:**
        - Historical sales data with daily granularity
        - Feature engineering for temporal patterns
        - Model training on historical data
        - Future prediction generation
        """)

# Instructions for running the app
if __name__ == "__main__":
    st.markdown("""
    ## 🚀 Getting Started
    
    **To run this interactive dashboard:**
    
    1. **Install required packages:**
    ```bash
    pip install streamlit plotly pandas scikit-learn numpy
    ```
    
    2. **Run the application:**
    ```bash
    streamlit run interactive_forecast_app.py
    ```
    
    3. **Open your browser** to the displayed URL (usually http://localhost:8501)
    
    **Note:** This app will create sample data if the sales_data.csv file is not found.
    Run the previous files first to use your own data!
    """)
    
    # Run the main app
    main()