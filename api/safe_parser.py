import requests
import sqlite3
import time
import json
from datetime import datetime

# Конфигурация
API_KEY = '005b8a3887ac4870920d909a7e31c7c5'
BASE_URL = 'http://api.football-data.org/v4'
HEADERS = {'X-Auth-Token': API_KEY}
DELAY = 6.1  # 10 запросов в минуту
DB_PATH = '/storage/emulated/0/FOOTBALL/db/football.db'
DATA_DIR = '/storage/emulated/0/FOOTBALL/data/raw'

def create_tables():
    """Создает необходимые таблицы в БД"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS teams (
                 id INTEGER PRIMARY KEY,
                 name TEXT UNIQUE,
                 short_name TEXT,
                 venue TEXT,
                 latitude REAL,
                 longitude REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS matches (
                 id INTEGER PRIMARY KEY,
                 home_team_id INTEGER,
                 away_team_id INTEGER,
                 date TEXT,
                 status TEXT,
                 home_score INTEGER,
                 away_score INTEGER,
                 FOREIGN KEY(home_team_id) REFERENCES teams(id),
                 FOREIGN KEY(away_team_id) REFERENCES teams(id))''')
    
    conn.commit()
    conn.close()

def safe_request(url):
    """Безопасный запрос с обработкой ошибок"""
    time.sleep(DELAY)
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка запроса {url}: {str(e)}")
        return None

def process_team(team_data):
    """Обрабатывает данные команды"""
    if isinstance(team_data, str):
        return None
        
    venue = team_data.get('venue', {})
    return {
        'id': team_data.get('id'),
        'name': team_data.get('name'),
        'short_name': team_data.get('shortName'),
        'venue': venue.get('name'),
        'latitude': venue.get('latitude'),
        'longitude': venue.get('longitude')
    }

def save_to_db(data, table_name):
    """Сохраняет данные в SQLite"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    for item in data:
        columns = ', '.join(item.keys())
        placeholders = ', '.join(['?'] * len(item))
        query = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
        c.execute(query, tuple(item.values()))
    
    conn.commit()
    conn.close()

def main():
    create_tables()
    
    # Пример для Премьер-лиги (PL)
    league_code = "PL"
    print(f"Получаем данные для лиги {league_code}...")
    
    # Получаем команды
    teams_url = f"{BASE_URL}/competitions/{league_code}/teams"
    teams_data = safe_request(teams_url)
    
    if teams_data:
        processed_teams = [process_team(t) for t in teams_data.get('teams', [])]
        save_to_db([t for t in processed_teams if t], 'teams')
        print(f"Сохранено {len(processed_teams)} команд")
    
    # Получаем матчи
    matches_url = f"{BASE_URL}/competitions/{league_code}/matches"
    matches_data = safe_request(matches_url)
    
    if matches_data:
        print(f"Найдено {len(matches_data.get('matches', []))} матчей")
        # Здесь можно добавить обработку матчей
    
    print("Готово!")

if __name__ == "__main__":
    main()
