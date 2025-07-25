import requests
from datetime import datetime

class OptimizedOddsAnalyzer:
    def __init__(self):
        self.API_KEY = "ec12a73194mshdb70514a3026ab3p1fe9e1jsn2efcb9d80fa4"
        self.headers = {
            "X-RapidAPI-Key": self.API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        self.available_bets = {
            "match_winner": "Match Winner",
            "double_chance": "Double Chance"
        }
        self.odds = {}
        self.stats = {}

    def get_odds(self, fixture_id):
        try:
            url = "https://api-football-v1.p.rapidapi.com/v3/odds"
            params = {"fixture": fixture_id}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return self._parse_odds(response.json())
        except Exception as e:
            print(f"Ошибка получения коэффициентов: {e}")
            return None

    def _parse_odds(self, data):
        if not data.get("response"):
            return {}
            
        bookmakers = data["response"][0]["bookmakers"]
        parsed_odds = {}
        
        for bookmaker in bookmakers:
            for bet in bookmaker["bets"]:
                if bet["name"] in self.available_bets.values():
                    bet_type = next(k for k,v in self.available_bets.items() if v == bet["name"])
                    parsed_odds[bet_type] = {
                        'bookmaker': bookmaker["name"],
                        'values': [{'value': o["value"], 'odd': float(o["odd"])} for o in bet["values"]]
                    }
        return parsed_odds

    def analyze_match(self, fixture_id):
        """Анализ матча с выводом коэффициентов"""
        self.odds = self.get_odds(fixture_id)
        if not self.odds:
            print("Коэффициенты не найдены")
            return
            
        print("\nЛучшие коэффициенты:")
        for bet_type, odds_data in self.odds.items():
            best_odd = max(odds_data['values'], key=lambda x: x['odd'])
            print(f"{bet_type.replace('_', ' ').title()}: {best_odd['value']} @ {best_odd['odd']:.2f}")

    def add_fbref_data(self, stats):
        """Добавление статистики FBref"""
        self.stats = stats
        print("\nДобавлена статистика:")
        print(f"Удары: {stats['shots']}")
        print(f"Удары в створ: {stats['shots_on_target']}")
        print(f"% сейвов: {stats['gk_save_percent']}%")
