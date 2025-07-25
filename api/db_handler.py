import sqlite3
from datetime import datetime

# Используем абсолютный путь
DB_PATH = '/data/data/com.termux/files/home/storage/shared/FOOTBALL/db/football.db'

def save_match(match_data):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO matches 
            (id, home_team_id, away_team_id, utc_date, status) 
            VALUES (?, ?, ?, ?, ?)
        ''', (
            match_data['id'],
            match_data['home_team_id'],
            match_data['away_team_id'],
            match_data.get('utc_date', datetime.now().isoformat()),
            match_data.get('status', 'SCHEDULED')
        ))
        conn.commit()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()
