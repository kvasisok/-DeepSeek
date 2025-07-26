import sqlite3

def show_stats():
    conn = sqlite3.connect("../data/matches.db")
    cursor = conn.cursor()
    
    # Топ-5 команд
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
    
    # Голы в последних матчах
    cursor.execute("SELECT home_team, home_goals FROM matches LIMIT 10")
    print("\n🎯 Последние матчи:")
    for team, goals in cursor.fetchall():
        print(f"{team.ljust(20)}: {'⚽' * goals}")

if __name__ == "__main__":
    show_stats()
