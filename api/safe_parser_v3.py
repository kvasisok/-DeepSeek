import requests
import sqlite3
import time
from datetime import datetime

# Конфигурация
FOOTBALL_API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
REQUEST_DELAY = 6.1

def get_db():
    return sqlite3.connect(DB_PATH)

def safe_request(url):
    """Безопасный запрос с обработкой ошибок"""
    time.sleep(REQUEST_DELAY)
    try:
        response = requests.get(url, headers={'X-Auth-Token': FOOTBALL_API_KEY})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка запроса {url}: {e}")
        return None

def safe_get(data, keys, default=None):
    """Рекурсивно получает данные из словаря"""
    if not isinstance(data, dict):
        return default
    for key in keys:
        try:
            data = data.get(key, default)
        except AttributeError:
            return default
    return data

def process_team(team):
    """Обработка данных команды с защитой от ошибок"""
    if not team or not isinstance(team, dict):
        return None
        
    try:
        venue = safe_get(team, ['venue'], {}) or {}
        return (
            safe_get(team, ['id']),
            str(safe_get(team, ['name'], '')).strip(),
            str(safe_get(team, ['shortName'], '')).strip(),
            str(safe_get(venue, ['name'], '')).strip(),
            float(safe_get(venue, ['latitude'], 0)) if safe_get(venue, ['latitude']) else None,
            float(safe_get(venue, ['longitude'], 0)) if safe_get(venue, ['longitude']) else None
        )
    except Exception as e:
        print(f"Ошибка обработки команды: {e}")
        return None

def process_match(match):
    """Обработка данных матча с защитой от ошибок"""
    if not match or not isinstance(match, dict):
        return None
        
    try:
        home_team = safe_get(match, ['homeTeam'], {})
        away_team = safe_get(match, ['awayTeam'], {})
        score = safe_get(match, ['score', 'fullTime'], {})
        
        match_date = safe_get(match, ['utcDate'], '')
        is_future = 1 if match_date and datetime.fromisoformat(match_date) > datetime.now() else 0
        
        return (
            safe_get(match, ['id']),
            safe_get(home_team, ['id']),
            safe_get(away_team, ['id']),
            match_date,
            str(safe_get(match, ['status'], '')).strip(),
            int(safe_get(score, ['home'], 0)),
            int(safe_get(score, ['away'], 0)),
            0,  # weather_updated
            is_future
        )
    except Exception as e:
        print(f"Ошибка обработки матча: {e}")
        return None

def main():
    db = get_db()
    cursor = db.cursor()
    
    # Инициализация БД
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            short_name TEXT,
            venue_name TEXT,
            venue_lat REAL,
            venue_lng REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY,
            home_team_id INTEGER,
            away_team_id INTEGER,
            utc_date TEXT,
            status TEXT,
            home_score INTEGER,
            away_score INTEGER,
            weather_updated INTEGER DEFAULT 0,
            is_future INTEGER DEFAULT 0,
            FOREIGN KEY(home_team_id) REFERENCES teams(id),
            FOREIGN KEY(away_team_id) REFERENCES teams(id)
        )
    ''')
    
    # Получаем данные Premier League
    print("Получаем команды...")
    teams_data = safe_request("http://api.football-data.org/v4/competitions/PL/teams")
    if teams_data:
        teams = [t for t in (process_team(team) for team in safe_get(teams_data, ['teams'], [])) if t]
        cursor.executemany('INSERT OR IGNORE INTO teams VALUES (?,?,?,?,?,?)', teams)
        print(f"Добавлено {len(teams)} команд")
    
    print("Получаем матчи...")
    matches_data = safe_request("http://api.football-data.org/v4/competitions/PL/matches")
    if matches_data:
        matches = [m for m in (process_match(match) for match in safe_get(matches_data, ['matches'], [])) if m]
        cursor.executemany('INSERT OR REPLACE INTO matches VALUES (?,?,?,?,?,?,?,?,?)', matches)
        print(f"Добавлено {len(matches)} матчей")
    
    db.commit()
    db.close()
    print("Парсинг завершен успешно!")

if __name__ == "__main__":
    main()
