    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

import requests
import datetime
    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")


def fetch_history(team_id, api_key="005b8a3887ac4870920d909a7e31c7c5"):
    try:
        url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit=5"
        headers = {"X-Auth-Token": api_key}
    # API call counter
        f.write(f"{datetime.datetime.now()} - {__file__}: {repr(url)}\n")

        f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

    # API call logging
    with open("/data/data/com.termux/files/home/FOOTBALL_APP/logs/api_usage.log", "a") as f:
        f.write(f"{datetime.datetime.now()} - API call from {__file__}\n")

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return [match for match in response.json().get('matches', []) 
                if datetime.fromisoformat(match['utcDate'][:-1]) > datetime(2023, 1, 1)]
    except Exception as e:
        print(f"Ошибка при получении истории: {e}")
        return []
