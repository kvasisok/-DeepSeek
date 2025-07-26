import sqlite3
import math
from datetime import datetime

class ProAnalyzer:
    def __init__(self):
        self.db_path = "../data/pro_matches_2025.db"
        
    def predict_match(self, home_team, away_team):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Проверяем наличие данных
        cursor.execute("SELECT COUNT(*) FROM matches WHERE home_team = ? OR away_team = ?", 
                      (home_team, away_team))
        match_count = cursor.fetchone()[0]
        
        if match_count < 3:
            return {"error": "Недостаточно данных для анализа"}
        
        # Получаем средние показатели
        cursor.execute("""
            SELECT 
                AVG(home_xg), AVG(away_xg),
                AVG(home_shots), AVG(away_shots)
            FROM matches
            WHERE home_team = ? AND status = 'Match Finished'
        """, (home_team,))
        home_data = cursor.fetchone()
        
        cursor.execute("""
            SELECT 
                AVG(away_xg), AVG(home_xg),
                AVG(away_shots), AVG(home_shots)
            FROM matches
            WHERE away_team = ? AND status = 'Match Finished'
        """, (away_team,))
        away_data = cursor.fetchone()
        
        conn.close()
        
        # Если нет данных xG
        if not home_data[0] or not away_data[0]:
            return {"error": "Нет данных xG для этих команд"}
        
        # Прогнозируемые показатели
        home_xg = (home_data[0] + away_data[1]) / 2
        away_xg = (away_data[0] + home_data[1]) / 2
        
        # Расчет вероятностей
        probs = self._calculate_probabilities(home_xg, away_xg)
        
        # Формирование отчета
        return {
            "teams": f"{home_team} vs {away_team}",
            "predicted_xg": f"{home_xg:.2f} - {away_xg:.2f}",
            "probabilities": probs,
            "recommendations": self._generate_recommendations(home_xg, away_xg, probs)
        }
    
    def _calculate_probabilities(self, home_xg, away_xg):
        """Расчет вероятностей исходов"""
        home_win = 0
        draw = 0
        away_win = 0
        
        for i in range(0, 6):  # Голы домашней
            for j in range(0, 6):  # Голы гостей
                prob = (math.exp(-home_xg) * (home_xg**i) / math.factorial(i)) * \
                       (math.exp(-away_xg) * (away_xg**j) / math.factorial(j))
                
                if i > j:
                    home_win += prob
                elif i == j:
                    draw += prob
                else:
                    away_win += prob
        
        return {
            "home_win": round(home_win * 100, 1),
            "draw": round(draw * 100, 1),
            "away_win": round(away_win * 100, 1)
        }
    
    def _generate_recommendations(self, home_xg, away_xg, probs):
        """Генерация рекомендаций"""
        rec = []
        total_xg = home_xg + away_xg
        
        if probs["home_win"] > 50:
            rec.append("П1 (Победа хозяев)")
        elif probs["away_win"] > 50:
            rec.append("П2 (Победа гостей)")
        
        if probs["draw"] > 30:
            rec.append("Х (Ничья)")
        
        if total_xg > 2.5:
            rec.append("ТБ 2.5 (Тотал больше 2.5)")
        elif total_xg < 1.5:
            rec.append("ТМ 1.5 (Тотал меньше 1.5)")
        
        return rec if rec else ["Нет четких рекомендаций"]

def main():
    analyzer = ProAnalyzer()
    
    print("=== PRO АНАЛИЗ МАТЧА ===")
    home = input("Хозяева: ").strip()
    away = input("Гости: ").strip()
    
    result = analyzer.predict_match(home, away)
    
    print("\nРезультат анализа:")
    if "error" in result:
        print(result["error"])
    else:
        print(f"Матч: {result['teams']}")
        print(f"Прогноз xG: {result['predicted_xg']}")
        print("\nВероятности:")
        print(f"П1: {result['probabilities']['home_win']}%")
        print(f"Х: {result['probabilities']['draw']}%")
        print(f"П2: {result['probabilities']['away_win']}%")
        print("\nРекомендации:", ", ".join(result['recommendations']))

if __name__ == "__main__":
    main()
