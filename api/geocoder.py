import sqlite3
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="football_app")

def update_coordinates():
    conn = sqlite3.connect('/storage/emulated/0/FOOTBALL/db/football.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, venue_name FROM teams WHERE venue_lat IS NULL AND venue_name != ''")
    
    for team_id, team_name, venue_name in cursor.fetchall():
        try:
            print(f"Поиск координат для: {venue_name}")
            location = geolocator.geocode(f"{venue_name}, UK")
            time.sleep(1)  # Чтобы не превысить лимиты geopy
            
            if location:
                cursor.execute('''
                    UPDATE teams SET
                        venue_lat = ?,
                        venue_lng = ?
                    WHERE id = ?
                ''', (location.latitude, location.longitude, team_id))
                print(f"Найдены координаты: {location.latitude}, {location.longitude}")
            else:
                print("Координаты не найдены")
                
        except Exception as e:
            print(f"Ошибка для {venue_name}: {str(e)}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_coordinates()
