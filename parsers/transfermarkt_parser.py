    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

import requests
import datetime
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

from bs4 import BeautifulSoup
import random
import datetime
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

import time
import datetime
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")


def get_injuries(team_url):
    try:
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Linux; Android 10)',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0)'
            ]),
            'Accept-Language': 'en-US,en;q=0.9'
        }
        time.sleep(random.uniform(2, 5))
        
        # Новый URL с проверкой доступности
        url = f"https://www.transfermarkt.com{team_url}/verletztespieler"
    # API call counter
        f.write(f"{datetime.datetime.now()} - {__file__}: {repr(url)}\n")

        f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    # API call logging
    with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        injured_players = []
        for row in soup.select('.items tbody tr'):
            name = row.select_one('.hauptlink a')
            if name:
                injured_players.append(name.text.strip())
                
        return injured_players
        
    except Exception as e:
        print(f"Ошибка парсинга Transfermarkt: {str(e)}")
        return []
