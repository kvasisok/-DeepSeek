import sqlite3

def show_top_teams():
    conn = sqlite3.connect("../data/matches.db")
    cursor = conn.cursor()
    
    # Топ-5 команд по победам
    cursor.execute("""
        SELECT 
            home_team,
            SUM(home_goals > away_goals) as wins,
            COUNT(*) as matches
        FROM matches
        GROUP BY home_team
        ORDER BY wins DESC
        LIMIT 5
    """)
    
    print("╔════════════════════════════╗")
    print("║       ТОП-5 КОМАНД       ║")
    print("╠══════════════╦═════╦══════╣")
    print("║ Команда      ║ Поб ║ Игр  ║")
    for row in cursor.fetchall():
        team, wins, matches = row
        print(f"║ {team.ljust(12)} ║ {str(wins).center(3)} ║ {str(matches).center(4)} ║")
    print("╚══════════════╩═════╩══════╝")

def show_goals_diff():
    conn = sqlite3.connect("../data/matches.db")
    cursor = conn.cursor()
    
    # Разница голов
    cursor.execute("""
        SELECT 
            home_team,
            SUM(home_goals) - SUM(away_goals) as diff
        FROM matches
        GROUP BY home_team
        ORDER BY diff DESC
        LIMIT 5
    """)
    
    print("\n📊 Лучшая разница голов (дом):")
    for team, diff in cursor.fetchall():
        print(f"{team.ljust(20)}: {'+' if diff > 0 else ''}{diff}")

def show_last_matches():
    conn = sqlite3.connect("../data/matches.db")
    cursor = conn.cursor()
    
    # Последние матчи
    cursor.execute("""
        SELECT 
            home_team, 
            home_goals, 
            away_team, 
            away_goals
        FROM matches
        ORDER BY date DESC
        LIMIT 5
    """)
    
    print("\n⚽ Последние матчи:")
    for row in cursor.fetchall():
        home, h_goals, away, a_goals = row
        print(f"{home.ljust(15)} {h_goals}:{a_goals} {away}")

if __name__ == "__main__":
    show_top_teams()
    show_goals_diff()
    show_last_matches()
