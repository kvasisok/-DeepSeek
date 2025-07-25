import requests
from datetime import datetime

class OddsAnalyzer:
    def __init__(self):
        self.API_KEY = "ec12a73194mshdb70514a3026ab3p1fe9e1jsn2efcb9d80fa4"
        self.headers = {
            "X-RapidAPI-Key": self.API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        self.log_file = "/data/data/com.termux/files/home/FOOTBALL_APP/logs/odds.log"
    
    def log(self, message):
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.now()} - {message}\n")

    def get_odds(self, fixture_id):
        """Получаем коэффициенты для матча"""
        try:
            url = "https://api-football-v1.p.rapidapi.com/v3/odds"
            params = {"fixture": fixture_id}
            self.log(f"Запрос коэффициентов для матча {fixture_id}")
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return self.parse_odds(response.json())
        except Exception as e:
            self.log(f"Ошибка: {str(e)}")
            return None

    def parse_odds(self, data):
        """Анализ коэффициентов"""
        if not data.get("response"):
            return None
            
        results = []
        for bookmaker in data["response"][0]["bookmakers"]:
            for bet in bookmaker["bets"]:
                for odd in bet["values"]:
                    results.append({
                        "bookmaker": bookmaker["name"],
                        "type": bet["name"],
                        "value": odd["value"],
                        "odd": float(odd["odd"])
                    })
        return results

    def get_top_odds(self, fixture_id, bet_type="Match Winner", limit=3):
        """Топ коэффициентов по типу ставки"""
        odds = self.get_odds(fixture_id)
        if not odds:
            return None
            
        filtered = [o for o in odds if o["type"] == bet_type]
        return sorted(filtered, key=lambda x: x["odd"], reverse=True)[:limit]

if __name__ == "__main__":
    analyzer = OddsAnalyzer()
    
    # Анализируем последний матч из логов (можете заменить ID)
    test_fixture = 1369607
    
    print(f"Анализ матча ID: {test_fixture}")
    
    # 1. Получаем топ коэффициентов на победу
    print("\nТоп-3 коэффициентов на победу:")
    winner_odds = analyzer.get_top_odds(test_fixture)
    if winner_odds:
        for odd in winner_odds:
            print(f"{odd['bookmaker']}: {odd['value']} @ {odd['odd']:.2f}")
    else:
        print("Данные не найдены")
    
    # 2. Получаем топ коэффициентов на тотал
    print("\nТоп-3 коэффициентов на тотал:")
    total_odds = analyzer.get_top_odds(test_fixture, "Over/Under")
    if total_odds:
        for odd in total_odds:
            print(f"{odd['bookmaker']}: {odd['type']} {odd['value']} @ {odd['odd']:.2f}")
