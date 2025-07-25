import requests
import sqlite3

DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"

def get_matches():
    response = requests.get(
        "https://api.football-data.org/v4/matches",
        headers={"X-Auth-Token": ""}
    )
    return response.json()

def save_to_db(matches):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for match in matches['matches']:
        cursor.execute("""
            INSERT OR IGNORE INTO matches 
            VALUES (?, ?, ?, ?)
        """, (
            match['id'],
            match['homeTeam']['id'],
            match['awayTeam']['id'],
            match['utcDate']
        ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    matches = get_matches()
    save_to_db(matches)
    print(f"Добавлено {len(matches['matches'])} матчей")
