import sqlite3
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class FootballAnalyzer2025:
    def __init__(self):
        self.db_path = "../data/matches_2025.db"
        self.api_key = os.getenv("API_KEY")
        self.api_host = "api-football-v1.p.rapidapi.com"
        self.current_year = 2025
        self.init_db()

    def init_db(self):
        """Инициализация новой базы для 2025 года"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                league_id INTEGER,
                season INTEGER,
                round TEXT,
                home_team TEXT,
                away_team TEXT,
                date TEXT,
                home_goals INTEGER,
                away_goals INTEGER,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def safe_request(self, url, params=None):
        """Безопасный запрос с обработкой кодировки"""
        headers = {
            "X-RapidAPI-Key": self.api_key.encode('ascii', 'ignore').decode('ascii'),
            "X-RapidAPI-Host": self.api_host
        }
        
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=15
            )
            response.encoding = 'utf-8'
            return response
        except Exception as e:
            print(f"Ошибка запроса: {type(e).__name__}")
            return None

    def fetch_current_season(self, league_id=39):
        """Загрузка актуального сезона 2024/2025"""
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        params = {
            "league": league_id,
            "season": 2024,  # Текущий сезон 2024/2025
            "timezone": "Europe/Moscow"
        }
        
        response = self.safe_request(url, params)
        if not response:
            return None
            
        try:
            data = response.json()
            if "response" not in data:
                print("Ошибка: Неверный формат ответа API")
                return None
                
            # Фильтруем только матчи 2025 года
            current_matches = [
                m for m in data["response"] 
                if m["fixture"]["date"].startswith("2025")
            ]
            return current_matches
            
        except json.JSONDecodeError:
            print("Ошибка: Невалидный JSON в ответе")
            return None

    def save_matches(self, matches):
        """Сохранение с проверкой дубликатов"""
        if not matches:
            print("Нет новых матчей для сохранения")
            return
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        new_matches = 0
        existing_matches = 0
        
        for match in matches:
            try:
                fixture = match["fixture"]
                teams = match["teams"]
                goals = match["goals"]
                league = match["league"]
                round_info = match["league"].get("round", "Regular Season")
                
                cursor.execute("""
                    INSERT OR IGNORE INTO matches VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                """, (
                    fixture["id"],
                    league["id"],
                    league["season"],
                    round_info,
                    teams["home"]["name"],
                    teams["away"]["name"],
                    fixture["date"],
                    goals["home"],
                    goals["away"],
                    fixture["status"]["long"]
                ))
                
                if cursor.rowcount > 0:
                    new_matches += 1
                else:
                    existing_matches += 1
                    
            except Exception as e:
                print(f"Ошибка сохранения матча: {e}")
        
        conn.commit()
        conn.close()
        print(f"\nНовых матчей: {new_matches}, уже в базе: {existing_matches}")

    def get_team_form(self, team_name, last_matches=5):
        """Анализ формы команды с учётом текущего сезона"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT 
                    date, home_team, away_team, home_goals, away_goals
                FROM matches
                WHERE (home_team = ? OR away_team = ?)
                AND season = 2024
                ORDER BY date DESC
                LIMIT ?
            """, (team_name, team_name, last_matches))
            
            results = []
            for row in cursor.fetchall():
                date, home, away, hg, ag = row
                date_str = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m.%Y")
                
                if home == team_name:
                    result = "П" if hg > ag else "Н" if hg == ag else "В"
                    score = f"{hg}-{ag}"
                    vs = away
                else:
                    result = "П" if ag > hg else "Н" if ag == hg else "В"
                    score = f"{ag}-{hg}"
                    vs = f"[{home}]"
                
                results.append(f"{date_str} {result} {score} vs {vs}")
            
            return results if results else ["Нет данных о последних матчах"]
            
        except Exception as e:
            return [f"Ошибка: {str(e)}"]
        finally:
            conn.close()

def main_menu():
    analyzer = FootballAnalyzer2025()
    
    while True:
        print("\n⚽ Футбольный анализатор 2025")
        print("1. Загрузить актуальные матчи")
        print("2. Показать форму команды")
        print("3. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            print("\nЗагрузка матчей сезона 2024/2025...")
            matches = analyzer.fetch_current_season()
            if matches:
                analyzer.save_matches(matches)
                print(f"Всего матчей 2025 года: {len(matches)}")
            else:
                print("Не удалось загрузить данные. Проверьте:")
                print("- Подключение к интернету")
                print("- Актуальность API-ключа")
        
        elif choice == "2":
            team = input("Введите название команды: ").strip()
            if team:
                print(f"\nФорма команды {team}:")
                for match in analyzer.get_team_form(team):
                    print(f"• {match}")
            else:
                print("Необходимо ввести название команды")
        
        elif choice == "3":
            print("Завершение работы")
            break
            
        else:
            print("Неверный выбор, попробуйте снова")

if __name__ == "__main__":
    main_menu()
