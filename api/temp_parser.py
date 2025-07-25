import requests
import sqlite3
import time
from datetime import datetime

API_KEY = '005b8a3887ac4870920d909a7e31c7c5'
BASE_URL = 'http://api.football-data.org/v4'
HEADERS = {'X-Auth-Token': API_KEY}
REQUEST_DELAY = 6.1

def get_db_connection():
    return sqlite3.connect('/storage/emulated/0/FOOTBALL/db/football.db')

def get_teams(league_code):
    url = f"{BASE_URL}/competitions/{league_code}/teams"
    time.sleep(REQUEST_DELAY)
    response = requests.get(url, headers=HEADERS)
    return response.json().get('teams', []) if response else []

def save_teams(league_code):
    teams = get_teams(league_code)
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS teams
                 (name TEXT, league_code TEXT, stadium_lat REAL, stadium_lng REAL)''')
    
    for team in teams:
        c.execute("INSERT INTO teams VALUES (?,?,?,?)",
                 (team['name'], league_code,
                  team.get('venue', {}).get('latitude'),
                  team.get('venue', {}).get('longitude')))
    conn.commit()
    conn.close()
    print(f"Сохранено {len(teams)} команд для лиги {league_code}")

if __name__ == "__main__":
    save_teams("PL")  # Премьер-лига
    save_teams("BL1") # Бундеслига
