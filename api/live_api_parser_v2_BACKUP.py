import requests
from utils.db_connector import get_connection
# ... (остальной код из предыдущей версии)

def save_to_db(matches, league_code):
    conn = get_connection()
    cursor = conn.cursor()
    
    for match in matches:
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO matches 
                (league_code, home_team, away_team, home_goals, away_goals, match_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                league_code,
                match["homeTeam"]["name"],
                match["awayTeam"]["name"],
                match["score"]["fullTime"]["home"],
                match["score"]["fullTime"]["away"],
                match["utcDate"]
            ))
        except Exception as e:
            print(f"Ошибка сохранения матча {match['id']}: {e}")
    
    conn.commit()
    conn.close()

# В функции update_all_data():
# Заменяем save_data() на save_to_db()

def get_db_connection():
    """Устанавливает соединение с базой данных"""
    return sqlite3.connect('/storage/emulated/0/FOOTBALL/db/football.db')

def save_teams_to_db(teams, league_code):
    """Сохраняет данные команд (включая координаты стадиона) в БД"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Создаем таблицу teams, если ее нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            name TEXT PRIMARY KEY,
            league_code TEXT,
            stadium_lat REAL,
            stadium_lng REAL
        )
    ''')
    
    for team in teams:
        venue = team.get('venue', {})
        cursor.execute('''
            INSERT OR REPLACE INTO teams (name, league_code, stadium_lat, stadium_lng)
            VALUES (?, ?, ?, ?)
        ''', (
            team['name'],
            league_code,
            venue.get('latitude'),
            venue.get('longitude')
        ))
    conn.commit()
    conn.close()

# Модифицируем существующую функцию get_teams
def get_teams(league_code):
    """Получает команды лиги и сохраняет их в БД"""
    url = f"{BASE_URL}/competitions/{league_code}/teams"
    response = make_request(url)
    if response:
        teams = response.json().get('teams', [])
        save_teams_to_db(teams, league_code)
        return teams
    return []
