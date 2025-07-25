import requests
import sqlite3
import time

FOOTBALL_API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def safe_request(url):
    time.sleep(6.1)  # соблюдаем лимит API
    try:
        response = requests.get(url, headers={'X-Auth-Token': FOOTBALL_API_KEY})
        return response.json()
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def main():
    db = get_db()
    cursor = db.cursor()
    
    # Парсим Premier League (PL)
    print("Получаем команды...")
    teams_data = safe_request("http://api.football-data.org/v4/competitions/PL/teams")
    if teams_data:
        for team in teams_data.get('teams', []):
            cursor.execute('''
                INSERT OR IGNORE INTO teams (id, name) 
                VALUES (?, ?)
            ''', (team.get('id'), team.get('name')))
    
    print("Получаем матчи...")
    matches_data = safe_request("http://api.football-data.org/v4/competitions/PL/matches")
    if matches_data:
        for match in matches_data.get('matches', []):
            cursor.execute('''
                INSERT OR IGNORE INTO matches 
                (id, home_team_id, away_team_id, utc_date, status, home_score, away_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                match.get('id'),
                match.get('homeTeam', {}).get('id'),
                match.get('awayTeam', {}).get('id'),
                match.get('utcDate'),
                match.get('status'),
                match.get('score', {}).get('fullTime', {}).get('home'),
                match.get('score', {}).get('fullTime', {}).get('away')
            ))
    
    db.commit()
    db.close()
    print("Готово! Данные сохранены.")

if __name__ == "__main__":
    main()
