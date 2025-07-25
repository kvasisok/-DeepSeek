import requests
import sqlite3
import time

DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
API_URL = "https://api.football-data.org/v4/teams"

def process_venue(venue):
    """Безопасная обработка venue данных"""
    if isinstance(venue, str):
        return {'name': venue, 'id': None}
    if not isinstance(venue, dict):
        return {'name': 'Unknown Venue', 'id': None}
    return {
        'name': venue.get('name', 'Unknown Venue').strip(),
        'lat': venue.get('latitude'),
        'lng': venue.get('longitude'),
        'id': venue.get('id')
    }

def main():
    try:
        # Получаем данные с API
        response = requests.get(API_URL, headers={"X-Auth-Token": API_KEY})
        response.raise_for_status()
        teams_data = response.json()

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            for team in teams_data.get('teams', []):
                venue = process_venue(team.get('venue', {}))
                
                # Проверяем существование venue_id
                venue_id = venue.get('id')
                if venue_id is None:
                    # Пытаемся получить ID из существующих данных
                    cursor.execute("SELECT id FROM teams WHERE venue_name = ? LIMIT 1", (venue['name'],))
                    existing = cursor.fetchone()
                    venue_id = existing[0] if existing else None
                
                # Вставляем данные
                cursor.execute("""
                    INSERT OR REPLACE INTO teams 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    team['id'],                  # id
                    team['name'],                # name
                    team.get('shortName', ''),   # short_name
                    venue['name'],               # venue_name
                    venue.get('lat'),            # venue_lat
                    venue.get('lng'),            # venue_lng
                    venue_id,                    # venue_id
                    int(time.time())             # updated_at
                ))
            
            print(f"Успешно обновлено {len(teams_data.get('teams', []))} команд")
            return True
            
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--full-update", action="store_true")
    args = parser.parse_args()
    
    if args.full_update:
        main()
