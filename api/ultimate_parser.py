import requests
import sqlite3
import time
from datetime import datetime
import json

# Конфигурация
FOOTBALL_API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
WEATHER_API_KEY = "a1ec654deae246ee882145847250407"
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
REQUEST_DELAY = 6.1

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def safe_request(url, headers=None):
    """Безопасный HTTP-запрос"""
    time.sleep(REQUEST_DELAY)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка запроса {url}: {e}")
        return None

def process_team(team):
    """Обрабатывает данные команды"""
    if not team or not isinstance(team, dict):
        return None
        
    try:
        venue = team.get('venue', {}) or {}
        return {
            'id': team.get('id'),
            'name': team.get('name', '').strip(),
            'short_name': team.get('shortName', '').strip(),
            'venue_name': venue.get('name', '').strip(),
            'venue_lat': float(venue.get('latitude', 0)) if venue.get('latitude') else None,
            'venue_lng': float(venue.get('longitude', 0)) if venue.get('longitude') else None
        }
    except Exception as e:
        print(f"Ошибка обработки команды: {e}")
        return None

def save_teams(teams):
    """Сохраняет команды в БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for team in teams:
        team_data = process_team(team)
        if team_data:
            cursor.execute('''
                INSERT OR REPLACE INTO teams 
                (id, name, short_name, venue_name, venue_lat, venue_lng)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                team_data['id'],
                team_data['name'],
                team_data['short_name'],
                team_data['venue_name'],
                team_data['venue_lat'],
                team_data['venue_lng']
            ))
    
    conn.commit()
    conn.close()

def process_match(match):
    """Обрабатывает данные матча"""
    if not match or not isinstance(match, dict):
        return None
        
    try:
        score = match.get('score', {}).get('fullTime', {})
        return {
            'id': match.get('id'),
            'competition_id': match.get('competition', {}).get('id'),
            'home_team_id': match.get('homeTeam', {}).get('id'),
            'away_team_id': match.get('awayTeam', {}).get('id'),
            'utc_date': match.get('utcDate'),
            'status': match.get('status'),
            'home_score': score.get('home'),
            'away_score': score.get('away')
        }
    except Exception as e:
        print(f"Ошибка обработки матча: {e}")
        return None

def save_matches(matches):
    """Сохраняет матчи в БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for match in matches:
        match_data = process_match(match)
        if match_data:
            cursor.execute('''
                INSERT OR REPLACE INTO matches 
                (id, competition_id, home_team_id, away_team_id, utc_date, status, home_score, away_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                match_data['id'],
                match_data['competition_id'],
                match_data['home_team_id'],
                match_data['away_team_id'],
                match_data['utc_date'],
                match_data['status'],
                match_data['home_score'],
                match_data['away_score']
            ))
    
    conn.commit()
    conn.close()

def main():
    # Инициализация БД
    conn = get_db_connection()
    conn.close()
    
    # Лиги для парсинга
    leagues = ['PL', 'BL1', 'PD']  # Premier League, Bundesliga, La Liga
    
    for league_code in leagues:
        print(f"\nОбработка лиги {league_code}...")
        
        # Получаем команды
        teams_url = f"http://api.football-data.org/v4/competitions/{league_code}/teams"
        teams_data = safe_request(teams_url, headers={'X-Auth-Token': FOOTBALL_API_KEY})
        
        if teams_data and 'teams' in teams_data:
            print(f"Найдено {len(teams_data['teams'])} команд")
            save_teams(teams_data['teams'])
        
        # Получаем матчи
        matches_url = f"http://api.football-data.org/v4/competitions/{league_code}/matches"
        matches_data = safe_request(matches_url, headers={'X-Auth-Token': FOOTBALL_API_KEY})
        
        if matches_data and 'matches' in matches_data:
            print(f"Найдено {len(matches_data['matches'])} матчей")
            save_matches(matches_data['matches'])
    
    print("\nПарсинг завершен успешно!")

if __name__ == "__main__":
    main()
