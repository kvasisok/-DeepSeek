    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

import requests
import datetime
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")


def get_flashscore_odds(match_url):
    try:
    # API call counter
        f.write(f"{datetime.datetime.now()} - {__file__}: {repr(url)}\n")

        f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    # API call logging
    with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

        response = requests.get(
            f"https://www.flashscore.com/match/{match_url}/#/odds-comparison",
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 12)'}
        )
        # Анализ через регулярные выражения
        import re
        odds = re.findall(r'odd__price">(\d+\.\d+)<', response.text)
        return {
            '1': odds[0],
            'X': odds[1],
            '2': odds[2]
        } if len(odds) >=3 else {}
    except:
        return {}
