# module_integration.py
# Basic example of integrating different modules and libraries

import random
import datetime
import math

class WeatherSimulator:
    """Simulates weather data using random module"""
    
    def __init__(self):
        self.weather_types = ["sunny", "cloudy", "rainy", "snowy"]
    
    def get_random_temperature(self, season="spring"):
        """Generate random temperature based on season"""
        temp_ranges = {
            "spring": (50, 75),
            "summer": (70, 95),
            "fall": (45, 70),
            "winter": (20, 50)
        }
        
        min_temp, max_temp = temp_ranges.get(season, (50, 75))
        return random.randint(min_temp, max_temp)
    
    def get_random_weather(self):
        """Get random weather type"""
        return random.choice(self.weather_types)

class DateTimeHelper:
    """Helper class using datetime module"""
    
    def get_current_info(self):
        """Get current date and time information"""
        now = datetime.datetime.now()
        return {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "month": now.strftime("%B")
        }
    
    def get_season(self, month=None):
        """Determine season based on month"""
        if month is None:
            month = datetime.datetime.now().month
            
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "fall"

class MathCalculator:
    """Math operations using math module"""
    
    def calculate_wind_chill(self, temp_f, wind_speed_mph):
        """Calculate wind chill factor"""
        if temp_f > 50 or wind_speed_mph < 3:
            return temp_f  # Wind chill not applicable
        
        # Wind chill formula
        wind_chill = (35.74 + (0.6215 * temp_f) - 
                     (35.75 * math.pow(wind_speed_mph, 0.16)) + 
                     (0.4275 * temp_f * math.pow(wind_speed_mph, 0.16)))
        
        return round(wind_chill, 1)
    
    def celsius_to_fahrenheit(self, celsius):
        """Convert celsius to fahrenheit"""
        return round((celsius * 9/5) + 32, 1)

class WeatherReport:
    """Integration class that combines all weather-related functionality"""
    
    def __init__(self):
        self.weather_sim = WeatherSimulator()
        self.date_helper = DateTimeHelper()
        self.math_calc = MathCalculator()
    
    def generate_daily_report(self):
        """Generate a complete weather report"""
        # Get current date info
        date_info = self.date_helper.get_current_info()
        current_month = datetime.datetime.now().month
        season = self.date_helper.get_season(current_month)
        
        # Generate weather data
        temperature = self.weather_sim.get_random_temperature(season)
        weather_type = self.weather_sim.get_random_weather()
        wind_speed = random.randint(0, 25)
        
        # Calculate additional metrics
        wind_chill = self.math_calc.calculate_wind_chill(temperature, wind_speed)
        temp_celsius = round((temperature - 32) * 5/9, 1)
        
        # Create comprehensive report
        report = f"""
Weather Report for {date_info['day_of_week']}, {date_info['date']}
Generated at: {date_info['time']}

Current Season: {season.title()}
Weather Condition: {weather_type.title()}
Temperature: {temperature}°F ({temp_celsius}°C)
Wind Speed: {wind_speed} mph
Wind Chill: {wind_chill}°F
"""
        
        return report.strip()

# Example usage
if __name__ == "__main__":
    print("Testing individual components:")
    
    # Test WeatherSimulator
    weather_sim = WeatherSimulator()
    print(f"Random temperature: {weather_sim.get_random_temperature('summer')}°F")
    print(f"Random weather: {weather_sim.get_random_weather()}")
    
    # Test DateTimeHelper
    date_helper = DateTimeHelper()
    current_info = date_helper.get_current_info()
    print(f"Today is {current_info['day_of_week']}, {current_info['date']}")
    
    # Test MathCalculator
    math_calc = MathCalculator()
    print(f"Wind chill at 30°F with 10mph wind: {math_calc.calculate_wind_chill(30, 10)}°F")
    
    print("\n" + "="*50)
    print("INTEGRATED WEATHER REPORT:")
    print("="*50)
    
    # Test integrated WeatherReport
    weather_report = WeatherReport()
    daily_report = weather_report.generate_daily_report()
    print(daily_report)