from bs4 import BeautifulSoup
import random, time, requests

def get_squad(team_id):
    try:
        headers = {'User-Agent': random.choice([
            'Mozilla/5.0 (Linux; Android 10)',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0)'
        ])}
        time.sleep(3)
        url = f"https://www.transfermarkt.com/team/startseite/verein/{team_id}"
        r = requests.get(url, headers=headers)
        return r.text if r.status_code == 200 else f"Error: {r.status_code}"
    except Exception as e:
        return f"Request failed: {str(e)}"
