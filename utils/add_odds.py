import csv
from pathlib import Path
from datetime import datetime
import shutil

def validate_odds(home, draw, away):
    if not all(odd > 1.0 for odd in [home, draw, away]):
        raise ValueError("Коэффициенты должны быть > 1.0")

def update_odds(match_id, home_team, away_team, home_win, draw, away_win):
    validate_odds(home_win, draw, away_win)
    db_path = Path(__file__).parent.parent / 'db' / 'odds.csv'
    temp_path = db_path.with_suffix('.tmp')
    
    updated = False
    with open(db_path, 'r') as infile, open(temp_path, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            if row and row[0] == match_id:
                writer.writerow([match_id, home_team, away_team, 
                               home_win, draw, away_win,
                               datetime.now().strftime('%Y-%m-%d %H:%M')])
                updated = True
            else:
                writer.writerow(row)
        
        if not updated:
            writer.writerow([match_id, home_team, away_team,
                           home_win, draw, away_win,
                           datetime.now().strftime('%Y-%m-%d %H:%M')])
    
    shutil.move(str(temp_path), str(db_path))

def update_odds(match_id, home_team, away_team, home_win, draw, away_win):
    db_path = Path(__file__).parent.parent / 'db' / 'odds.csv'
    if not db_path.exists():
        with open(db_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['match_id','home_team','away_team',
                           'home_win','draw','away_win','last_update'])
    # ... остальная реализация ...
