import sqlite3
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class FootballAnalyzer:
    def __init__(self):
        self.db_path = "../data/basic_matches_2025.db"
        self.api_key = os.getenv("API_KEY")
        self.api_host = os.getenv("API_HOST")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                home_team TEXT,
                away_team TEXT,
                date TEXT,
                home_goals INTEGER,
                away_goals INTEGER,
                home_shots INTEGER,
                away_shots INTEGER,
                status TEXT
            )
        """)
        conn.commit()
        conn.close()

    def update_matches(self):
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {"league": 39, "season": 2024}
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            data = response.json()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for match in data.get("response", []):
                if not match["fixture"]["date"].startswith("2025"):
                    continue
                
                cursor.execute("""
                    INSERT OR REPLACE INTO matches VALUES (?,?,?,?,?,?,?,?,?)
                """, (
                    match["fixture"]["id"],
                    match["teams"]["home"]["name"],
                    match["teams"]["away"]["name"],
                    match["fixture"]["date"],
                    match["goals"]["home"],
                    match["goals"]["away"],
                    match["statistics"]["shots"]["home"] if "statistics" in match else 0,
                    match["statistics"]["shots"]["away"] if "statistics" in match else 0,
                    match["fixture"]["status"]["long"]
                ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Ошибка: {e}")
            return False

    def predict_match(self, home_team, away_team):
        """Прогноз на основе базовой статистики"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Получаем средние показатели
        cursor.execute("""
            SELECT 
                AVG(home_goals), AVG(away_goals),
                AVG(home_shots), AVG(away_shots)
            FROM matches
            WHERE home_team = ? AND status = 'Match Finished'
        """, (home_team,))
        home_stats = cursor.fetchone()
        
        cursor.execute("""
            SELECT 
                AVG(away_goals), AVG(home_goals),
                AVG(away_shots), AVG(home_shots)
            FROM matches
            WHERE away_team = ? AND status = 'Match Finished'
        """, (away_team,))
        away_stats = cursor.fetchone()
        
        conn.close()
        
        if not home_stats or not away_stats:
            return "Недостаточно данных"
        
        # Прогнозируемые голы (простая модель)
        pred_home = (home_stats[0] + away_stats[1]) / 2
        pred_away = (away_stats[0] + home_stats[1]) / 2
        
        return f"Прогноз: {home_team} {round(pred_home, 1)} - {round(pred_away, 1)} {away_team}"

if __name__ == "__main__":
    analyzer = FootballAnalyzer()
    
    print("1. Обновить данные")
    print("2. Прогноз матча")
    choice = input("Выберите: ")
    
    if choice == "1":
        if analyzer.update_matches():
            print("✅ Данные обновлены")
        else:
            print("❌ Ошибка")
    elif choice == "2":
        home = input("Хозяева: ")
        away = input("Гости: ")
        print(analyzer.predict_match(home, away))
