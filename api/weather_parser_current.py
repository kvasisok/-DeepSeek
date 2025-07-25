import sqlite3
import requests
from datetime import datetime
import time
import logging

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

def get_current_weather(lat, lon):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={lat},{lon}"
        logger.info(f"Current weather API URL: {url}")
        
        time.sleep(REQUEST_DELAY)
        response = requests.get(url, timeout=10)
        logger.info(f"API Response Status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"API Error: {response.text}")
            return None
            
        data = response.json()
        current = data['current']
        return {
            'temp_c': current['temp_c'],
            'condition': current['condition']['text'],
            'wind_kph': current['wind_kph'],
            'humidity': current['humidity'],
            'precip_mm': current.get('precip_mm', 0),
            'last_updated': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting current weather: {str(e)}")
        return None

def update_weather_for_matches():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT 
            m.id, 
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
        match_id, lat, lon, home_team = match
        logger.info(f"Processing match {match_id} at {lat},{lon}")
        
        weather = get_current_weather(lat, lon)
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
