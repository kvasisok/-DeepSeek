#!/bin/bash
cd /storage/emulated/0/FOOTBALL

echo "=== Запуск основного парсера ==="
python api/football_parser.py

echo "=== Запуск погодного парсера ==="
python api/weather_parser.py

echo "=== Проверка результатов ==="
sqlite3 db/football.db << 'SQL'
SELECT 
    m.id,
    (SELECT name FROM teams WHERE id = m.home_team_id) as home_team,
    (SELECT name FROM teams WHERE id = m.away_team_id) as away_team,
    w.temp_c,
    w.condition
FROM matches m
LEFT JOIN weather_data w ON m.id = w.match_id
WHERE m.status = 'FINISHED'
LIMIT 5;
SQL
