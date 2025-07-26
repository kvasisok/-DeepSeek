import sqlite3
import matplotlib.pyplot as plt

def plot_top_teams():
    conn = sqlite3.connect("../data/matches.db")
    cursor = conn.cursor()
    
    # Получаем топ-5 команд по победам дома
    cursor.execute("""
        SELECT 
            home_team,
            SUM(CASE WHEN home_goals > away_goals THEN 1 ELSE 0 END) as wins
        FROM matches
        GROUP BY home_team
        ORDER BY wins DESC
        LIMIT 5
    """)
    
    teams = []
    wins = []
    for row in cursor.fetchall():
        teams.append(row[0])
        wins.append(row[1])
    
    # Строим график
    plt.figure(figsize=(10, 5))
    plt.bar(teams, wins, color='green')
    plt.title('Топ-5 команд по домашним победам')
    plt.ylabel('Количество побед')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('../stats/top_teams.png')
    print("График сохранен: ../stats/top_teams.png")

if __name__ == "__main__":
    plot_top_teams()
