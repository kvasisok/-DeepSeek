import sqlite3
import argparse

DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"

def update_match(match_id):
    # Здесь будет логика обновления конкретного матча
    print(f"Обновление данных матча {match_id}...")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--match-id", type=int, required=True)
    args = parser.parse_args()
    update_match(args.match_id)
