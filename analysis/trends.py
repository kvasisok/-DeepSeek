def analyze_trends(predictions):
    """Анализ изменения прогнозов со временем"""
    from statistics import mean
    return {
        'avg_home': mean(p.get('home', 0) for p in predictions),
        'trend': '↑' if predictions[-1]['home'] > predictions[0]['home'] else '↓'
    }
