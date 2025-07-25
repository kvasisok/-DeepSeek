import requests
import sqlite3
import time

FOOTBALL_API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
REQUEST_DELAY = 6.1

def update_team_details():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Получаем список команд без координат
    cursor.execute("SELECT id FROM teams WHERE venue_lat IS NULL OR venue_lng IS NULL")
    team_ids = [row[0] for row in cursor.fetchall()]
    
    for team_id in team_ids:
        time.sleep(REQUEST_DELAY)
        try:
            url = f"http://api.football-data.org/v4/teams/{team_id}"
            response = requests.get(url, headers={'X-Auth-Token': FOOTBALL_API_KEY})
            data = response.json()
            
            venue = data.get('venue', {})
            cursor.execute('''
                UPDATE teams SET
                    venue_name = ?,
                    venue_lat = ?,
                    venue_lng = ?
                WHERE id = ?
            ''', (
                venue.get('name', ''),
                venue.get('latitude'),
                venue.get('longitude'),
                team_id
            ))
            print(f"Обновлена команда ID {team_id}")
        except Exception as e:
            print(f"Ошибка для команды {team_id}: {e}")
    
    conn.commit()
    conn.close()
    print("Обновление завершено!")

if __name__ == "__main__":
    update_team_details()
