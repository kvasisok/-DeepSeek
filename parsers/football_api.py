import requests
import json
from datetime import datetime

class FootballAPI:
    def __init__(self):
        self.API_KEY = "ec12a73194mshdb70514a3026ab3p1fe9e1jsn2efcb9d80fa4"
        self.headers = {
            "X-RapidAPI-Key": self.API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        self.log_file = "/data/data/com.termux/files/home/FOOTBALL_APP/logs/api.log"
        
    def log(self, message):
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.now()} - {message}\n")

    def get_data(self, endpoint, params={}):
        """Универсальный метод для запросов"""
        try:
            url = f"https://api-football-v1.p.rapidapi.com/v3/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.log(f"Error in {endpoint}: {str(e)}")
            return None

    def get_live_matches(self):
        """Получаем текущие live-матчи"""
        data = self.get_data("fixtures", {"live": "all"})
        if data and data.get("response"):
            return [{
                "id": match["fixture"]["id"],
                "teams": f"{match['teams']['home']['name']} vs {match['teams']['away']['name']}",
                "league": match["league"]["name"]
            } for match in data["response"]]
        return []

    def get_odds(self, fixture_id):
        """Получаем коэффициенты для матча"""
        return self.get_data("odds", {"fixture": fixture_id})

if __name__ == "__main__":
    api = FootballAPI()
    
    # 1. Получаем live-матчи
    live_matches = api.get_live_matches()
    print(f"Найдено live-матчей: {len(live_matches)}")
    
    # 2. Для каждого матча проверяем коэффициенты
    for match in live_matches[:3]:  # Проверяем первые 3 матча
        print(f"\nМатч: {match['teams']} ({match['league']})")
        odds = api.get_odds(match["id"])
        if odds:
            print("Коэффициенты:", json.dumps(odds, indent=2))
        else:
            print("Коэффициенты недоступны")
