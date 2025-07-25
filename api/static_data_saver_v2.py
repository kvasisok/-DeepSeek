import sqlite3
import requests
import json
import time
from datetime import datetime

FOOTBALL_API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
REQUEST_DELAY = 6.1

def safe_get(data, keys, default=None):
    """Безопасное получение данных из словаря"""
    if not isinstance(data, dict):
        return default
    for key in keys:
        try:
            data = data.get(key, default)
            if data is None:
                return default
        except AttributeError:
            return default
    return data

def process_venue(venue_data):
    """Обработка данных стадиона"""
    if isinstance(venue_data, str):
        return {'name': venue_data}
    if not isinstance(venue_data, dict):
        return {}
    return {
        'id': safe_get(venue_data, ['id']),
        'name': str(safe_get(venue_data, ['name'], '')).strip(),
        'city': str(safe_get(venue_data, ['city'], '')).strip(),
        'capacity': safe_get(venue_data, ['capacity']),
        'surface': str(safe_get(venue_data, ['grass'], 'natural')).strip(),
        'lat': safe_get(venue_data, ['latitude']),
        'lng': safe_get(venue_data, ['longitude'])
    }

def save_static_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создаем таблицы, если их нет
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS venues (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT,
            capacity INTEGER,
            surface TEXT,
            lat REAL,
            lng REAL,
            last_updated TEXT
        );
        
        CREATE TABLE IF NOT EXISTS teams_static (
            team_id INTEGER PRIMARY KEY,
            founded INTEGER,
            club_colors TEXT,
            venue_id INTEGER,
            FOREIGN KEY(venue_id) REFERENCES venues(id)
        );
        
        CREATE TABLE IF NOT EXISTS api_cache (
            endpoint TEXT PRIMARY KEY,
            data TEXT,
            last_updated TEXT
        );
    ''')
    
    # Получаем список всех команд
    cursor.execute("SELECT id, name FROM teams")
    teams = cursor.fetchall()
    
    for team_id, team_name in teams:
        print(f"Обработка команды: {team_name} (ID: {team_id})")
        
        try:
            # Получаем данные команды
            url = f"http://api.football-data.org/v4/teams/{team_id}"
            response = requests.get(url, headers={'X-Auth-Token': FOOTBALL_API_KEY})
            response.raise_for_status()
            data = response.json()
            
            # Сохраняем сырые данные в кэш
            cursor.execute('''
                INSERT OR REPLACE INTO api_cache
                VALUES (?, ?, ?)
            ''', (url, json.dumps(data), datetime.now().isoformat()))
            
            # Обрабатываем venue
            venue_data = safe_get(data, ['venue'], {})
            venue = process_venue(venue_data)
            
            if venue:
                cursor.execute('''
                    INSERT OR REPLACE INTO venues VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    venue['id'],
                    venue['name'],
                    venue['city'],
                    venue['capacity'],
                    venue['surface'],
                    venue['lat'],
                    venue['lng'],
                    datetime.now().isoformat()
                ))
            
            # Сохраняем статические данные команды
            cursor.execute('''
                INSERT OR REPLACE INTO teams_static VALUES
                (?, ?, ?, ?)
            ''', (
                team_id,
                safe_get(data, ['founded']),
                str(safe_get(data, ['clubColors'], '')).strip(),
                venue.get('id')
            ))
            
            # Обновляем ссылку на venue в основной таблице
            if venue.get('id'):
                cursor.execute('''
                    UPDATE teams SET venue_id = ? WHERE id = ?
                ''', (venue['id'], team_id))
            
            print(f"Успешно сохранено: {team_name}")
            
        except Exception as e:
            print(f"Ошибка для команды {team_id}: {str(e)}")
        
        time.sleep(REQUEST_DELAY)
    
    conn.commit()
    conn.close()
    print("Все статические данные сохранены!")

if __name__ == "__main__":
    save_static_data()
