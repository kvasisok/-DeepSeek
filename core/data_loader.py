import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_HOST = "api-football-v1.p.rapidapi.com"

def fetch_fixtures(league_id=39, season=2023):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    params = {"league": league_id, "season": season}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

def save_to_db(data):
    conn = sqlite3.connect("../data/matches.db")
    cursor = conn.cursor()
    
    # Удаляем старую таблицу (если нужно)
    cursor.execute("DROP TABLE IF EXISTS matches")
    
    # Создаем новую таблицу с правильной структурой
    cursor.execute("""
        CREATE TABLE matches (
            id INTEGER PRIMARY KEY,
            league_id INTEGER,
            home_team TEXT,
            away_team TEXT,
            date TEXT,
            home_goals INTEGER,
            away_goals INTEGER
        )
    """)
    
    for match in data:
        fixture = match["fixture"]
        teams = match["teams"]
        goals = match["goals"]
        league = match["league"]
        
        cursor.execute("""
            INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            fixture["id"],
            league["id"],
            teams["home"]["name"],
            teams["away"]["name"],
            fixture["date"],
            goals["home"],
            goals["away"]
        ))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Загрузка матчей...")
    matches = fetch_fixtures()
    if matches:
        save_to_db(matches)
        print(f"Сохранено матчей: {len(matches)}")
    else:
        print("Ошибка загрузки данных")
