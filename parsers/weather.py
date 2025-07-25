import requests
from utils.cache import get_cache, set_cache

WEATHER_API_KEY = "a1ec654deae246ee882145847250407"

def get_weather(lat, lon, match_time):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={lat},{lon}"
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def analyze_weather_impact(weather_data):
    if not weather_data or 'current' not in weather_data:
        return 0.0
    
    current = weather_data['current']
    impact = 0.0
    
    # Точные критерии оценки
    weather_codes = {
        'rain': [1063, 1180, 1186, 1192],
        'storm': [1087, 1273, 1276],
        'snow': [1114, 1210, 1219]
    }
    
    code = current.get('condition', {}).get('code', 1000)
    
    if code in weather_codes['rain']:
        impact += 1.5 + current.get('precip_mm', 0)/10
    elif code in weather_codes['storm']:
        impact += 2.0
    elif code in weather_codes['snow']:
        impact += 2.5
    
    if current.get('wind_kph', 0) > 20:
        impact += 1.0
    
    return min(3.5, impact)
