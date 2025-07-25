import sqlite3
import requests
import time
from datetime import datetime

FOOTBALL_API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
LEAGUES = ['PL']  # Начнем только с Premier League для теста

def get_db():
    return sqlite3.connect(DB_PATH)

def safe_request(url):
    time.sleep(6.1)
    try:
        response = requests.get(url, headers={'X-Auth-Token': FOOTBALL_API_KEY})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request error: {e}")
        return None

def get_coordinates_for_team(team_name):
    """Возвращает примерные координаты для известных стадионов"""
    stadium_coords = {
        'Arsenal FC': (51.5549, -0.108436),
        'Aston Villa': (52.5092, -1.8848),
        'Chelsea FC': (51.4817, -0.1910),
        # Добавьте другие команды по необходимости
    }
    return stadium_coords.get(team_name, (None, None))

def update_teams_and_stadiums(league_code):
    db = get_db()
    data = safe_request(f"http://api.football-data.org/v4/competitions/{league_code}/teams")
    
    if data and 'teams' in data:
        for team in data['teams']:
            # Сохраняем команду
            db.execute('''
                INSERT OR REPLACE INTO teams (id, name, short_name)
                VALUES (?, ?, ?)
            ''', (
                team['id'],
                team['name'],
                team.get('shortName', '')
            ))
            
            # Получаем координаты
            lat, lon = get_coordinates_for_team(team['name'])
            
            # Сохраняем стадион (даже если координаты None)
            db.execute('''
                INSERT OR REPLACE INTO stadiums 
                (team_id, name, latitude, longitude)
                VALUES (?, ?, ?, ?)
            ''', (
                team['id'],
                team.get('venue', 'Unknown'),
                lat,
                lon
            ))
        db.commit()
    db.close()

def update_matches(league_code):
    db = get_db()
    data = safe_request(f"http://api.football-data.org/v4/competitions/{league_code}/matches")
    
    if data and 'matches' in data:
        for match in data['matches']:
            score = match.get('score', {}).get('fullTime', {})
            db.execute('''
                INSERT OR REPLACE INTO matches 
                (id, home_team_id, away_team_id, utc_date, status, home_score, away_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                match['id'],
                match['homeTeam']['id'],
                match['awayTeam']['id'],
                match['utcDate'],
                match['status'],
                score.get('home'),
                score.get('away')
            ))
        db.commit()
    db.close()

def main():
    for league in LEAGUES:
        print(f"Updating {league}...")
        update_teams_and_stadiums(league)
        update_matches(league)
    print("Football data update complete!")

if __name__ == "__main__":
    main()
