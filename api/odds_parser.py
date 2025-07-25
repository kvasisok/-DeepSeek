import sqlite3
import requests

DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"

def get_active_matches():
    """Получает матчи без коэффициентов"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id 
        FROM matches m
        LEFT JOIN betting_odds b ON m.id = b.match_id
        WHERE b.match_id IS NULL
        AND m.status = 'SCHEDULED'
        LIMIT 5
    """)
    matches = cursor.fetchall()
    conn.close()
    return [m[0] for m in matches]

def fetch_odds(match_id):
    """Заглушка для реального API"""
    print(f"Получаю коэффициенты для матча {match_id}...")
    return {
        'match_id': match_id,
        'home_win': 1.85,
        'draw': 3.40,
        'away_win': 4.20
    }

def save_odds(odds):
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            INSERT INTO betting_odds 
            VALUES (?, ?, ?, ?)
        """, (odds['match_id'], odds['home_win'], odds['draw'], odds['away_win']))
        conn.commit()
        print(f"Сохранены коэффициенты для матча {odds['match_id']}")
    except sqlite3.Error as e:
        print(f"Ошибка сохранения: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("=== Старт парсинга коэффициентов ===")
    matches = get_active_matches()
    if not matches:
        print("Нет матчей для обновления")
    else:
        for match_id in matches:
            odds = fetch_odds(match_id)
            if odds:
                save_odds(odds)
    print("=== Парсинг завершен ===")
