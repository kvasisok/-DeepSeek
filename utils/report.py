from utils.colors import TermColors as tc

def generate_report(match, probabilities):
    """Генерация отчета с таблицей коэффициентов"""
    return f"""
{tc.HEADER}=== ПРОГНОЗ МАТЧА ==={tc.ENDC}

⚽ {tc.BOLD}{match['home_team']} vs {match['away_team']}{tc.ENDC}
📅 Дата: {match['date']} | 🕒 Время: {match['time']} (UTC+4)
🏆 Турнир: {match['competition']}

{tc.UNDERLINE}КОЭФФИЦИЕНТЫ:{tc.ENDC}
┌──────────┬──────────┬────────────┐
│  Исход   │ Коэфф.   │ Вероятность│
├──────────┼──────────┼────────────┤
│ {tc.WARNING}П1{tc.ENDC}     │ {match['home_odd']:<8} │ {probabilities['home']:>6.1f}%   │
│ {tc.WARNING}Ничья{tc.ENDC}  │ {match['draw_odd']:<8} │ {probabilities['draw']:>6.1f}%   │
│ {tc.WARNING}П2{tc.ENDC}     │ {match['away_odd']:<8} │ {probabilities['away']:>6.1f}%   │
└──────────┴──────────┴────────────┘

{tc.UNDERLINE}РЕКОМЕНДАЦИИ:{tc.ENDC}
• {tc.OKGREEN}Основная ставка:{tc.ENDC} {get_main_tip(probabilities)}
• {tc.OKBLUE}Альтернатива:{tc.ENDC} {get_alternative_tip(probabilities)}
• {tc.WARNING}Экспресс:{tc.ENDC} {get_express_tip(probabilities)}
"""

def get_main_tip(probs):
    if probs['home'] > 60: return "Победа хозяев (П1)"
    if probs['away'] > 60: return "Победа гостей (П2)"
    if probs['draw'] > 40: return "Ничья (X)"
    return "Анализ неоднозначен"

def get_alternative_tip(probs):
    if abs(probs['home'] - probs['away']) < 15:
        return "Фора 0 (0)"
    return "Тотал > 2.5"

def get_express_tip(probs):
    if probs['home'] > 55 and probs['draw'] > 30:
        return "П1 + ТБ 1.5"
    if probs['away'] > 55 and probs['draw'] > 30:
        return "П2 + ТБ 1.5"
    return "Не рекомендуется"
