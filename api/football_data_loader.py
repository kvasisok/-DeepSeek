import requests
def get_matches():
    return requests.get("https://api.football-data.org/v4/matches").json()
