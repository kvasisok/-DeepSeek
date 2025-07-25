import datetime
with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

import os
with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

import datetime
with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

import json
with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

import requests
with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

CACHE_TIME = 3600
TIMEZONE_OFFSET = timedelta(hours=4)

def get_football_headers():
    return {'X-Auth-Token': os.getenv('FOOTBALL_API_KEY')}

def _convert_to_utc4(utc_time_str):
    try:
        dt = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
        return (dt + TIMEZONE_OFFSET).strftime("%Y-%m-%d %H:%M")
    except:
        return utc_time_str[:16]

def fetch_live_matches(force_refresh=False):
    cache_file = Path(__file__).parent.parent / 'db' / 'matches_cache.json'
    
    if not force_refresh and cache_file.exists():
        cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if cache_age < timedelta(seconds=CACHE_TIME):
            return _read_cache(cache_file)
    
    try:
        response = requests.get(
            f"{os.getenv('FOOTBALL_API_URL')}/matches",
            headers=get_football_headers(),
            timeout=10
        )
        response.raise_for_status()
        matches = _process_matches(response.json().get('matches', []))
        _save_cache(cache_file, matches)
        return matches
    except Exception as e:
        print(f"API Error: {e}")
        return _read_cache(cache_file) if cache_file.exists() else []

def _process_matches(matches):
    processed = []
    for match in matches:
        if match.get('status') in ['SCHEDULED', 'TIMED']:
            date_utc4 = _convert_to_utc4(match['utcDate'])
            processed.append({
                'id': match['id'],
                'date': date_utc4[:10],
                'time': date_utc4[11:16],
                'datetime': date_utc4,
                'home_team': match['homeTeam']['name'],
                'away_team': match['awayTeam']['name'],
                'home_odd': match.get('odds', {}).get('homeWin', 2.5),
                'draw_odd': match.get('odds', {}).get('draw', 3.2),
                'away_odd': match.get('odds', {}).get('awayWin', 2.8),
                'competition': match['competition']['name']
            })
    return processed

def _save_cache(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)

def _read_cache(file):
    with open(file) as f:
        return json.load(f)

def get_team_matches(team_name):
    """Улучшенный поиск по командам"""
    matches = fetch_live_matches()
    return [
        m for m in matches 
        if team_name.lower() in m['home_team'].lower() 
        or team_name.lower() in m['away_team'].lower()
    ]

def get_unique_teams():
    matches = fetch_live_matches()
    return sorted({m['home_team'] for m in matches} | {m['away_team'] for m in matches})
