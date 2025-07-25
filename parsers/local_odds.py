import csv
from utils.add_odds import add_odds

def parse_odds(filepath):
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_odds(
                row['match_id'],
                row['home_team'],
                row['away_team'],
                float(row['home_win']),
                float(row['draw']),
                float(row['away_win'])
            )
