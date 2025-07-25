import sqlite3
import requests
from time import sleep

DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"

def safe_db_query(query, params=()):
    """Выполняет запрос с обработкой ошибок"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка БД: {e}")
        return None
    finally:
        if conn:
            conn.close()

def fetch_team_players(team_id):
    """Заглушка для реального парсинга"""
    print(f"Получаю состав команды {team_id}...")
    sleep(1)  # Имитация запроса
    return [
        (1, team_id, 5, 3),  # player_id, team_id, goals, assists
        (2, team_id, 2, 7)
    ]

def main():
    teams = safe_db_query("SELECT id FROM teams")
    if not teams:
        print("Не найдено команд в БД")
        return

    for (team_id,) in teams:
        players = fetch_team_players(team_id)
        if not players:
            continue
            
        for player in players:
            safe_db_query("""
                INSERT OR REPLACE INTO player_stats 
                VALUES (?, ?, ?, ?)
            """, player)
        print(f"Обновлено {len(players)} игроков команды {team_id}")

if __name__ == "__main__":
    print("=== Старт обновления статистики игроков ===")
    main()
    print("=== Обновление завершено ===")
