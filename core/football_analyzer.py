import sqlite3
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class FootballAnalyzer:
    def __init__(self):
        self.db_path = "../data/matches_2025.db"
        self.api_key = os.getenv("API_KEY")
        self.api_host = os.getenv("API_HOST")
        self.current_year = 2025
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS matches")
        cursor.execute("""
            CREATE TABLE matches (
                id INTEGER PRIMARY KEY,
                league_id INTEGER,
                season INTEGER,
                home_team TEXT,
                away_team TEXT,
                match_date TEXT,
                home_goals INTEGER,
                away_goals INTEGER,
                status TEXT
            )
        """)
        conn.commit()
        conn.close()

    def update_matches(self):
        try:
            response = requests.get(
                f"https://{self.api_host}/v3/fixtures",
                headers={
                    "X-RapidAPI-Key": self.api_key,
                    "X-RapidAPI-Host": self.api_host
                },
                params={"league": 39, "season": 2024},
                timeout=10
            )
            data = response.json()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for match in data.get("response", []):
                fixture = match["fixture"]
                if not fixture["date"].startswith("2025"):
                    continue
                
                cursor.execute("""
                    INSERT OR REPLACE INTO matches VALUES (?,?,?,?,?,?,?,?,?)
                """, (
                    fixture["id"],
                    match["league"]["id"],
                    match["league"]["season"],
                    match["teams"]["home"]["name"],
                    match["teams"]["away"]["name"],
                    fixture["date"],
                    match["goals"]["home"],
                    match["goals"]["away"],
                    fixture["status"]["long"]
                ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_team_form(self, team_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT match_date, home_team, away_team, home_goals, away_goals
            FROM matches
            WHERE (home_team = ? OR away_team = ?)
            ORDER BY match_date DESC
            LIMIT 5
        """, (team_name, team_name))
        
        results = []
        for row in cursor.fetchall():
            date, home, away, hg, ag = row
            date_str = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z").strftime("%d.%m")
            result = "W" if (home == team_name and hg > ag) or (away == team_name and ag > hg) else "D" if hg == ag else "L"
            opponent = away if home == team_name else home
            results.append(f"{date_str} {result} {hg}-{ag} vs {opponent}")
        
        conn.close()
        return results

def main_menu():
    analyzer = FootballAnalyzer()
    
    while True:
        print("\n1. Update matches")
        print("2. Team form")
        print("3. Exit")
        choice = input("Select: ").strip()
        
        if choice == "1":
            print("Updating...")
            if analyzer.update_matches():
                print("Success!")
            else:
                print("Failed")
        
        elif choice == "2":
            team = input("Team name: ").strip()
            print("\n".join(analyzer.get_team_form(team)))
        
        elif choice == "3":
            break

if __name__ == "__main__":
    main_menu()
