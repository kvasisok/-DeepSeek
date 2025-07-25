import requests
from datetime import datetime

class AdvancedOddsAnalyzer:
    def __init__(self):
        self.API_KEY = "ec12a73194mshdb70514a3026ab3p1fe9e1jsn2efcb9d80fa4"
        self.headers = {
            "X-RapidAPI-Key": self.API_KEY,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        self.bet_types = {
            "match_winner": "Match Winner",
            "double_chance": "Double Chance",
            "over_under": "Over/Under",
            "corners_winner": "Corners Match Winner",
            "corners_over": "Corners Over/Under",
            "cards_winner": "Cards Match Winner",
            "cards_over": "Cards Over/Under"
        }

    def get_odds(self, fixture_id):
        """Получаем все коэффициенты для матча"""
        try:
            url = "https://api-football-v1.p.rapidapi.com/v3/odds"
            params = {"fixture": fixture_id}
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return self._parse_odds(response.json())
        except Exception as e:
            print(f"Ошибка: {e}")
            return None

    def _parse_odds(self, data):
        """Парсим ответ API"""
        if not data.get("response"):
            return None
            
        bookmakers = data["response"][0]["bookmakers"]
        parsed_odds = []
        
        for bookmaker in bookmakers:
            for bet in bookmaker["bets"]:
                if bet["name"] in self.bet_types.values():
                    for odd in bet["values"]:
                        parsed_odds.append({
                            "bookmaker": bookmaker["name"],
                            "type": bet["name"],
                            "value": odd["value"],
                            "odd": float(odd["odd"])
                        })
        return parsed_odds

    def get_top_odds(self, fixture_id, bet_category):
        """Получаем топ-3 коэффициента по категории"""
        odds = self.get_odds(fixture_id)
        if not odds:
            return None
            
        bet_type = self.bet_types[bet_category]
        filtered = [o for o in odds if o["type"] == bet_type]
        
        # Специальная обработка для Over/Under
        if "over" in bet_category:
            filtered = [o for o in filtered if "Over" in o["value"]]
        elif "under" in bet_category:
            filtered = [o for o in filtered if "Under" in o["value"]]
        
        return sorted(filtered, key=lambda x: x["odd"], reverse=True)[:3]

    def analyze_match(self, fixture_id):
        """Полный анализ матча"""
        print(f"\nАнализ матча ID: {fixture_id}")
        
        # 1. Победитель матча
        print("\n1. Топ коэффициентов на победу:")
        winner = self.get_top_odds(fixture_id, "match_winner")
        self._print_odds(winner)
        
        # 2. Двойной шанс (не проиграет)
        print("\n2. Топ коэффициентов на двойной шанс:")
        double_chance = self.get_top_odds(fixture_id, "double_chance")
        self._print_odds(double_chance)
        
        # 3-4. Тоталы
        print("\n3. Топ коэффициентов на ТБ (2.5):")
        over = self.get_top_odds(fixture_id, "over_under")
        self._print_odds(over)
        
        print("\n4. Топ коэффициентов на ТМ (2.5):")
        under = self.get_top_odds(fixture_id, "over_under")
        self._print_odds(under)
        
        # 5-7. Угловые
        print("\n5. Топ коэффициентов на победу по угловым:")
        corners_winner = self.get_top_odds(fixture_id, "corners_winner")
        self._print_odds(corners_winner)
        
        print("\n6. Топ коэффициентов на ТБ угловых (9.5):")
        corners_over = self.get_top_odds(fixture_id, "corners_over")
        self._print_odds(corners_over)
        
        print("\n7. Топ коэффициентов на ТМ угловых (9.5):")
        corners_under = self.get_top_odds(fixture_id, "corners_over")
        self._print_odds(corners_under)
        
        # 8-10. Карточки
        print("\n8. Топ коэффициентов на победу по карточкам:")
        cards_winner = self.get_top_odds(fixture_id, "cards_winner")
        self._print_odds(cards_winner)
        
        print("\n9. Топ коэффициентов на ТБ карточек (4.5):")
        cards_over = self.get_top_odds(fixture_id, "cards_over")
        self._print_odds(cards_over)
        
        print("\n10. Топ коэффициентов на ТМ карточек (4.5):")
        cards_under = self.get_top_odds(fixture_id, "cards_over")
        self._print_odds(cards_under)

    def _print_odds(self, odds):
        """Вывод коэффициентов"""
        if odds:
            for odd in odds:
                print(f"{odd['bookmaker']}: {odd['value']} @ {odd['odd']:.2f}")
        else:
            print("Данные не найдены")

if __name__ == "__main__":
    analyzer = AdvancedOddsAnalyzer()
    test_fixture = 1369607  # Замените на актуальный ID
    analyzer.analyze_match(test_fixture)
