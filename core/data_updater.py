import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DataUpdater:
    def __init__(self):
        self.db_path = "../data/pro_matches_2025.db"
        self.api_key = os.getenv("API_KEY")
        self.api_host = os.getenv("API_HOST")
        self._init_db()

    def _init_db(self):
        """Инициализация новой базы с правильной структурой"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS matches")
        
        cursor.execute("""
            CREATE TABLE matches (
                id INTEGER PRIMARY KEY,
                home_team TEXT,
                away_team TEXT,
                date TEXT,
                home_xg REAL DEFAULT 0,
                away_xg REAL DEFAULT 0,
                home_shots INTEGER DEFAULT 0,
                away_shots INTEGER DEFAULT 0,
                status TEXT
            )
        """)
        conn.commit()
        conn.close()

    def update_matches(self):
        """Обновленная версия загрузки данных"""
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {
            "league": 39,
            "season": 2024,
            "from": "2025-01-01",
            "to": "2025-12-31"
        }
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }

        try:
            print("Загрузка списка матчей...")
            fixtures_response = requests.get(url, headers=headers, params=params, timeout=15)
            fixtures_response.raise_for_status()
            fixtures = fixtures_response.json().get("response", [])

            if not fixtures:
                print("Нет данных о матчах")
                return False

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            total_updated = 0
            
            for fixture in fixtures:
                match_id = fixture["fixture"]["id"]
                
                # Пропускаем если матч не в 2025 году
                if not fixture["fixture"]["date"].startswith("2025"):
                    continue
                
                # Получаем расширенную статистику
                stats = self._get_match_stats(match_id)
                
                if not stats:
                    continue
                
                # Сохраняем данные
                cursor.execute("""
                    INSERT OR REPLACE INTO matches VALUES (?,?,?,?,?,?,?,?,?)
                """, (
                    match_id,
                    fixture["teams"]["home"]["name"],
                    fixture["teams"]["away"]["name"],
                    fixture["fixture"]["date"],
                    stats["home_xg"],
                    stats["away_xg"],
                    stats["home_shots"],
                    stats["away_shots"],
                    fixture["fixture"]["status"]["long"]
                ))
                total_updated += 1
            
            conn.commit()
            conn.close()
            print(f"Успешно обновлено матчей: {total_updated}")
            return True
            
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return False

    def _get_match_stats(self, match_id):
        """Получение статистики матча"""
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics"
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }
        
        try:
            response = requests.get(url, headers=headers, params={"fixture": match_id}, timeout=10)
            response.raise_for_status()
            stats_data = response.json().get("response", [])
            
            if len(stats_data) < 2:
                return None
            
            result = {
                "home_xg": 0,
                "away_xg": 0,
                "home_shots": 0,
                "away_shots": 0
            }
            
            # Определяем какая команда домашняя
            home_team_id = stats_data[0]["team"]["id"]
            
            for team_stats in stats_data:
                for stat in team_stats["statistics"]:
                    if stat["type"] == "Expected Goals":
                        if team_stats["team"]["id"] == home_team_id:
                            result["home_xg"] = float(stat["value"] or 0)
                        else:
                            result["away_xg"] = float(stat["value"] or 0)
                    elif stat["type"] == "Total Shots":
                        if team_stats["team"]["id"] == home_team_id:
                            result["home_shots"] = int(stat["value"] or 0)
                        else:
                            result["away_shots"] = int(stat["value"] or 0)
            
            return result
            
        except Exception as e:
            print(f"Ошибка получения статистики для матча {match_id}: {e}")
            return None

if __name__ == "__main__":
    updater = DataUpdater()
    if updater.update_matches():
        print("✅ Данные успешно обновлены")
    else:
        print("❌ Ошибка при обновлении данных")
