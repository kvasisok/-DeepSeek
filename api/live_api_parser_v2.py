import requests
import sqlite3
from datetime import datetime
import time
import os
from utils.db_connector import get_connection

API_KEY = '005b8a3887ac4870920d909a7e31c7c5'
BASE_URL = 'http://api.football-data.org/v4'
HEADERS = {'X-Auth-Token': API_KEY}
REQUEST_DELAY = 6.1
DATA_DIR = '/storage/emulated/0/FOOTBALL/data/raw'

def save_teams_to_db(teams, league_code):
    """Сохраняет команды в базу данных"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Создаем таблицу, если ее нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            name TEXT PRIMARY KEY,
            league_code TEXT,
            stadium_lat REAL,
            stadium_lng REAL
        )
    ''')
    
    for team in teams:
        venue = team.get('venue', {})
        cursor.execute('''
            INSERT OR REPLACE INTO teams (name, league_code, stadium_lat, stadium_lng)
            VALUES (?, ?, ?, ?)
        ''', (
            team['name'],
            league_code,
            venue.get('latitude'),
            venue.get('longitude')
        ))
    conn.commit()
    conn.close()

def make_request(url):
    """Выполняет запрос с задержкой"""
    time.sleep(REQUEST_DELAY)
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

def get_teams(league_code):
    """Получает список команд лиги"""
    url = f"{BASE_URL}/competitions/{league_code}/teams"
    response = make_request(url)
    if response:
        teams = response.json().get('teams', [])
        save_teams_to_db(teams, league_code)
        return teams
    return []

def get_matches(league_code):
    """Получает матчи лиги"""
    url = f"{BASE_URL}/competitions/{league_code}/matches"
    response = make_request(url)
    return response.json().get('matches', []) if response else []

def save_data(data, filename):
    """Сохраняет данные в JSON"""
    os.makedirs(DATA_DIR, exist_ok=True)
    data['last_updated'] = datetime.now().isoformat()
    with open(f'{DATA_DIR}/{filename}', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    leagues = {'PL': 'Premier League', 'BL1': 'Bundesliga'}  # Пример лиг
    for code, name in leagues.items():
        print(f"Обработка {name}...")
        teams = get_teams(code)
        matches = get_matches(code)
        save_data({'teams': teams, 'matches': matches}, f'{code}_data.json')
    print("Готово!")
