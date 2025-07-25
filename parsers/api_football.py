import requests
from utils.cache import get_cache, set_cache

def fetch_fixtures(league_id):
    cached = get_cache(f'fixtures_{league_id}')
    if cached: return cached['data']
    
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?league={league_id}"
    headers = {
        "X-RapidAPI-Key": "ваш_ключ",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        set_cache(f'fixtures_{league_id}', data)
        return data
    return None
