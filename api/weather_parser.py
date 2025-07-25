import sqlite3
import requests
from datetime import datetime
import time
import logging

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='/storage/emulated/0/FOOTBALL/logs/weather_parser.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

WEATHER_API_KEY = "a1ec654deae246ee882145847250407"
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
REQUEST_DELAY = 1

def get_db():
    return sqlite3.connect(DB_PATH)

def log_match_info(match_id, home_team, date, lat, lon):
    logger.info(f"Processing match: {match_id}")
    logger.info(f"Team: {home_team}, Date: {date}")
    logger.info(f"Coordinates: {lat}, {lon}")

def get_weather(lat, lon, date):
    try:
        # Преобразуем дату из формата ISO (2023-08-19T14:00:00Z)
        date_obj = datetime.strptime(date.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
        date_str = date_obj.strftime('%Y-%m-%d')
        
        url = f"http://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}&q={lat},{lon}&dt={date_str}"
        logger.info(f"Weather API URL: {url}")
        
        time.sleep(REQUEST_DELAY)
        response = requests.get(url, timeout=10)
        logger.info(f"API Response Status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"API Error: {response.text}")
            return None
            
        data = response.json()
        logger.info("Successfully received weather data")
        
        day = data['forecast']['forecastday'][0]['day']
        return {
            'temp_c': day['avgtemp_c'],
            'condition': day['condition']['text'],
            'wind_kph': day['maxwind_kph'],
            'humidity': day['avghumidity'],
            'precip_mm': day['totalprecip_mm'],
            'last_updated': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting weather: {str(e)}")
        return None

def update_weather_for_matches():
    db = get_db()
    cursor = db.cursor()
    
    # Получаем матчи для обновления
    cursor.execute('''
        SELECT 
            m.id, 
            m.utc_date, 
            s.latitude, 
            s.longitude,
            t.name
        FROM matches m
        JOIN stadiums s ON m.home_team_id = s.team_id
        JOIN teams t ON m.home_team_id = t.id
        WHERE m.status = 'FINISHED' 
        AND m.weather_updated = 0
        AND s.latitude IS NOT NULL
        AND s.longitude IS NOT NULL
        LIMIT 5
    ''')
    
    matches = cursor.fetchall()
    logger.info(f"Found {len(matches)} matches to update")
    
    updated = 0
    for match in matches:
        match_id, utc_date, lat, lon, home_team = match
        log_match_info(match_id, home_team, utc_date, lat, lon)
        
        weather = get_weather(lat, lon, utc_date)
        if weather:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO weather_data 
                    (match_id, temp_c, condition, wind_kph, humidity, precip_mm, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    match_id, 
                    weather['temp_c'], 
                    weather['condition'],
                    weather['wind_kph'], 
                    weather['humidity'],
                    weather['precip_mm'], 
                    weather['last_updated']
                ))
                
                cursor.execute('''
                    UPDATE matches SET weather_updated = 1 WHERE id = ?
                ''', (match_id,))
                db.commit()
                updated += 1
                logger.info(f"Successfully updated weather for match {match_id}")
            except Exception as e:
                logger.error(f"Database error for match {match_id}: {str(e)}")
                db.rollback()
        else:
            logger.warning(f"Weather data not available for match {match_id}")
    
    db.close()
    print(f"Weather data updated for {updated} matches")
    logger.info(f"Update completed. Total matches updated: {updated}")

if __name__ == "__main__":
    update_weather_for_matches()
