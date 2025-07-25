from parsers.odds_parser import get_odds_oddsportal as get_odds
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / 'configs' / 'api_config.json'

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

print("Конфиг загружен:", load_config()['base_url'])
