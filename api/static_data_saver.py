import sqlite3
import requests
import time  # Добавлен отсутствующий импорт
from geopy.geocoders import Nominatim

# Конфигурация
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
REQUEST_DELAY = 1  # Задержка между запросами (секунды)

def process_venue(venue_data):
    """Защищенная обработка venue данных"""
    if isinstance(venue_data, str):
        return {'name': venue_data}
    if not isinstance(venue_data, dict):
        return {'name': 'Unknown Venue'}
    return {
        'name': str(venue_data.get('name', 'Unknown Venue')).strip(),
        'lat': venue_data.get('latitude'),
        'lng': venue_data.get('longitude')
    }

def get_stadium_coordinates(venue_name):
    """Геокодинг для стадионов без координат"""
    try:
        geolocator = Nominatim(user_agent="football_app")
        location = geolocator.geocode(f"{venue_name}, football stadium")
        return (location.latitude, location.longitude) if location else (None, None)
    except Exception as e:
        print(f"Geocoding error for {venue_name}: {str(e)}")
        return (None, None)

def save_team_data(team):
    """Обновленная функция сохранения данных команды"""
    venue = process_venue(team.get('venue', {}))
    venue_name = venue.get('name', 'Unknown Venue')
    
    if venue.get('lat') is None or venue.get('lng') is None:
        lat, lng = get_stadium_coordinates(venue_name)
        venue.update({'lat': lat, 'lng': lng})
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO teams 
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            team['id'],
            team['name'],
            team.get('shortName', ''),
            venue_name,
            venue['lat'],
            venue['lng']
        ])

def fetch_teams_data():
    """Загрузка данных команд с API"""
    url = "https://api.football-data.org/v4/teams"
    headers = {"X-Auth-Token": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['teams']

def save_static_data():
    """Основная функция обновления"""
    teams = fetch_teams_data()
    for team in teams:
        try:
            save_team_data(team)
            time.sleep(REQUEST_DELAY)
        except Exception as e:
            print(f"Ошибка для команды {team.get('id', 'unknown')}: {str(e)}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-teams", action="store_true")
    args = parser.parse_args()
    
    if args.update_teams:
        save_static_data()
