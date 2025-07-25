from datetime import datetime

class MatchPredictor:
    def __init__(self):
        self.weather_impact = 0.0
        self.location = None
    
    def apply_weather(self, lat, lon, match_time):
        from parsers.weather import analyze_weather_impact, get_weather
        self.location = (lat, lon)
        weather_data = get_weather(lat, lon, match_time)
        self.weather_impact = analyze_weather_impact(weather_data)
    
    def predict(self, stats=None):
        stats = stats or {}
        base = {
            'home': 48.0,  # Базовое преимущество дома
            'draw': 30.0,
            'away': 22.0
        }
        
        # Учет xG-разницы
        xg_diff = stats.get('xg_diff', 0.0)
        base['home'] += xg_diff * 12
        base['away'] -= xg_diff * 10
        base['draw'] -= abs(xg_diff) * 2
        
        # Коррекция на погоду
        weather_effect = 1 + self.weather_impact * 0.12
        base['home'] *= weather_effect
        base['away'] /= weather_effect
        
        # Гарантированные пределы
        final = {
            'home': max(25.0, min(70.0, base['home'])),
            'draw': max(15.0, min(35.0, base['draw'])),
            'away': max(15.0, min(40.0, base['away']))
        }
        
        # Нормализация
        total = sum(final.values())
        return {k: round(v/total*100, 1) for k, v in final.items()}
