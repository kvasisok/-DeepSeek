import csv
from pathlib import Path
from difflib import get_close_matches

def load_teams():
    db_path = Path(__file__).parent.parent / 'db' / 'matches.csv'
    teams = set()
    with open(db_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            teams.add(row['home'])
            teams.add(row['away'])
    return sorted(teams)

def find_matches(team_name):
    db_path = Path(__file__).parent.parent / 'db' / 'matches.csv'
    matches = []
    with open(db_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if team_name in (row['home'], row['away']):
                matches.append(row)
    return matches

def search_team(user_input, teams):
    return get_close_matches(user_input, teams, n=3, cutoff=0.3)
