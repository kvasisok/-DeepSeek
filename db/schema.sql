CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY,
    home_team TEXT,
    away_team TEXT,
    timestamp DATETIME
);

CREATE TABLE IF NOT EXISTS predictions (
    match_id INTEGER,
    home_win_prob REAL,
    draw_prob REAL,
    away_win_prob REAL,
    FOREIGN KEY(match_id) REFERENCES matches(match_id)
);
