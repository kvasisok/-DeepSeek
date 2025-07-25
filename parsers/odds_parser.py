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


def get_odds(match):
    """Универсальный парсер для OddsPortal"""
    try:
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Android 12; Mobile)',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0)'
            ])
        }
        time.sleep(random.uniform(2, 5))
        
        url = f'https://www.oddsportal.com/matches/soccer/{match}/'
    # API call counter
        f.write(f"{datetime.datetime.now()} - {__file__}: {repr(url)}\n")

        f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    # API call logging
    with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

        response = requests.get(url, headers=headers, timeout=15)
        
        if '404 Page' in response.text:
            return {'error': 'Матч не найден'}
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            '1': soup.select_one('div.odds-1x2-1').text.strip(),
            'X': soup.select_one('div.odds-1x2-x').text.strip(),
            '2': soup.select_one('div.odds-1x2-2').text.strip(),
            'updated': soup.select_one('p.update-time').text.strip()
        }
    except Exception as e:
        return {'error': str(e)}
