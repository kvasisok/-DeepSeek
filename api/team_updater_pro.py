import requests
import sqlite3
import time
import json

FOOTBALL_API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
REQUEST_DELAY = 6.1

def safe_request(url):
    """Безопасный запрос с обработкой ошибок"""
    time.sleep(REQUEST_DELAY)
    try:
        response = requests.get(url, headers={'X-Auth-Token': FOOTBALL_API_KEY})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка запроса: {str(e)}")
        return None

def safe_get(data, keys, default=None):
    """Рекурсивное безопасное получение данных"""
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

def update_team_details():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Получаем список всех команд
    cursor.execute("SELECT id, name FROM teams")
    teams = cursor.fetchall()
    
    for team_id, team_name in teams:
        print(f"Обработка команды: {team_name} (ID: {team_id})")
        
        team_data = safe_request(f"http://api.football-data.org/v4/teams/{team_id}")
        if not team_data:
            continue
            
        # Обработка venue с максимальной защитой
        venue = {}
        try:
            if isinstance(team_data.get('venue'), dict):
                venue = team_data['venue']
            elif isinstance(team_data.get('venue'), str):
                venue = {'name': team_data['venue']}
        except Exception as e:
            print(f"Ошибка обработки venue: {str(e)}")
            venue = {}
            
        # Подготовка данных для обновления
        update_data = {
            'venue_name': str(safe_get(venue, ['name'], '')).strip(),
            'venue_lat': float(safe_get(venue, ['latitude'], 0)) if safe_get(venue, ['latitude']) else None,
            'venue_lng': float(safe_get(venue, ['longitude'], 0)) if safe_get(venue, ['longitude']) else None,
            'team_id': team_id
        }
        
        # Обновляем запись в БД
        cursor.execute('''
            UPDATE teams SET
                venue_name = :venue_name,
                venue_lat = :venue_lat,
                venue_lng = :venue_lng
            WHERE id = :team_id
        ''', update_data)
    
    conn.commit()
    conn.close()
    print("Все команды обработаны!")

if __name__ == "__main__":
    update_team_details()
