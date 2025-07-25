from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "/storage/emulated/0/FOOTBALL/db/football.db"
PROJECT_ROOT = "/storage/emulated/0/FOOTBALL/web"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, "static"), filename)

@app.route("/api/teams")
def teams():
    conn = get_db_connection()
    teams = conn.execute("SELECT id, name, short_name FROM teams").fetchall()
    conn.close()
    return jsonify([dict(team) for team in teams])

@app.route("/api/matches/<int:team_id>")
def team_matches(team_id):
    conn = get_db_connection()
    
    past_matches = conn.execute("""
        SELECT m.id, m.utc_date, t1.short_name as home_team, 
               m.home_score, t2.short_name as away_team, m.away_score
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.id
        JOIN teams t2 ON m.away_team_id = t2.id
        WHERE (m.home_team_id = ? OR m.away_team_id = ?)
        AND m.status = 'FINISHED'
        ORDER BY m.utc_date DESC LIMIT 5
    """, (team_id, team_id)).fetchall()
    
    future_matches = conn.execute("""
        SELECT m.id, m.utc_date, t1.short_name as home_team,
               t2.short_name as away_team
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.id
        JOIN teams t2 ON m.away_team_id = t2.id
        WHERE (m.home_team_id = ? OR m.away_team_id = ?)
        AND m.status = 'SCHEDULED'
        ORDER BY m.utc_date ASC LIMIT 5
    """, (team_id, team_id)).fetchall()
    
    conn.close()
    return jsonify({
        "past": [dict(match) for match in past_matches],
        "future": [dict(match) for match in future_matches]
    })

@app.route("/api/commands")
def get_commands():
    commands = [
        {"name": "Обновить данные", "command": "./update_all.sh"},
        {"name": "Создать бэкап", "command": "./backup_manager.sh"},
        {"name": "Открыть веб-интерфейс", "command": "termux-open-url http://127.0.0.1:8080"}
    ]
    return jsonify(commands)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
