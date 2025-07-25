import requests

api_key = "eaf68ffb413d707283399af330d02c3f"
lat = 40.7128  # New York City latitude
lon = -74.0060  # New York City longitude

url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"

response = requests.get(url)
data = response.json()

print(f"5-day forecast for coordinates ({lat}, {lon}):")
for item in data['list'][:5]:  # Show first 5 forecasts
    print(f"{item['dt_txt']}: {item['weather'][0]['description']}, {item['main']['temp']}°C")