from core_analyzer import MatchPredictor
predictor = MatchPredictor()
result = predictor.predict({})
print(f"Прогноз: П1 {result['home_win']:.0%} | Ничья {result['draw']:.0%} | П2 {result['away_win']:.0%}")
