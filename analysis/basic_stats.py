import sqlite3
import pandas as pd

def main():
    conn = sqlite3.connect('/storage/emulated/0/FOOTBALL/db/football.db')
    
    # Основная статистика
    stats = pd.read_sql('''
        SELECT 
            t.name as team,
            COUNT() as matches,
            SUM(CASE WHEN m.home_team_id = t.id AND m.home_score > m.away_score THEN 1
                     WHEN m.away_team_id = t.id AND m.away_score > m.home_score THEN 1
                     ELSE 0 END) as wins,
            SUM(CASE WHEN m.home_score = m.away_score THEN 1 ELSE 0 END) as draws
        FROM teams t
        LEFT JOIN matches m ON t.id IN (m.home_team_id, m.away_team_id)
        WHERE m.status = 'FINISHED'
        GROUP BY t.name
        ORDER BY wins DESC
    ''', conn)
    
    print("\nТурнирная таблица:\n")
    print(stats.to_string(index=False))
    
    # Средние показатели
    averages = pd.read_sql('''
        SELECT 
            AVG(home_score + away_score) as avg_goals,
            AVG(home_score) as avg_home_goals,
            AVG(away_score) as avg_away_goals
        FROM matches 
        WHERE status = 'FINISHED'
    ''', conn)
    
    print("\nСредние показатели:\n")
    print(averages.to_string(index=False))
    
    conn.close()

if __name__ == "__main__":
    main()
