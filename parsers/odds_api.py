import requests
import json
import datetime
import os

API_KEY = "ec12a73194mshdb70514a3026ab3p1fe9e1jsn2efcb9d80fa4"
LOG_DIR = "/data/data/com.termux/files/home/FOOTBALL_APP/logs"

def log_api(message):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(f"{LOG_DIR}/api.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - {message}\n")

def get_live_fixtures():
    """Получаем список актуальных матчей"""
    try:
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        params = {
            "league": 39,  # Premier League
            "season": 2023,
            "status": "live"
        }
        
        log_api("Fetching live fixtures")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["response"]
        
    except Exception as e:
        log_api(f"Error getting fixtures: {str(e)}")
        return []

def get_odds(fixture_id):
    """Получаем коэффициенты для конкретного матча"""
    try:
        url = "https://api-football-v1.p.rapidapi.com/v3/odds"
        headers = {
            "X-RapidAPI-Key": API_KEY, 
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        params = {
            "fixture": fixture_id,
            "bookmaker": 1,
            "bet": 1  # Ставка на исход матча
        }
        
        log_api(f"Fetching odds for fixture {fixture_id}")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        log_api(f"Error getting odds: {str(e)}")
        return None

if __name__ == "__main__":
    # Получаем актуальные матчи
    fixtures = get_live_fixtures()
    
    if fixtures:
        print("Live fixtures found:")
        for fixture in fixtures:
            print(f"ID: {fixture['fixture']['id']} | {fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}")
            
            # Получаем коэффициенты
            odds = get_odds(fixture['fixture']['id'])
            print(f"Odds: {json.dumps(odds, indent=2) if odds else 'No odds data'}")
    else:
        print("No live fixtures found")
