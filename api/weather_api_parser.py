import sqlite3
import requests
from time import sleep

DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
WEATHER_API_KEY = "a1ec654deae246ee882145847250407"

def fetch_weather(lat, lng, date):
    """Запрос погодных данных"""
    url = f"http://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}&q={lat},{lng}&dt={date}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка запроса погоды: {str(e)}")
        return None

def update_pending_matches():
    """Обновление погоды для матчей"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Получаем матчи без данных о погоде
        cursor.execute("""
            SELECT m.id, m.utc_date, t.venue_lat, t.venue_lng 
            FROM matches m
            JOIN teams t ON m.home_team_id = t.id
            WHERE m.weather_updated = 0 AND m.status = 'FINISHED'
            LIMIT 10
        """)
        
        matches = cursor.fetchall()
        
        for match_id, date, lat, lng in matches:
            if not lat or not lng:
                continue
                
            weather = fetch_weather(lat, lng, date[:10])
            if weather:
                day_data = weather['forecast']['forecastday'][0]['day']
                
                cursor.execute("""
                    INSERT OR REPLACE INTO weather_data
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    match_id,
                    day_data['avgtemp_c'],
                    day_data['condition']['text'],
                    day_data['maxwind_kph'],
                    day_data['avghumidity'],
                    day_data['totalprecip_mm']
                ))
                
                cursor.execute("""
                    UPDATE matches SET weather_updated = 1 WHERE id = ?
                """, (match_id,))
                
                conn.commit()
                print(f"Обновлена погода для матча {match_id}")
                sleep(1)  # Задержка между запросами

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-pending", action="store_true")
    args = parser.parse_args()
    
    if args.update_pending:
        update_pending_matches()
