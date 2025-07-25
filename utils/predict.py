def calculate_probabilities(home_odd, draw_odd, away_odd):
    total_margin = (1/home_odd + 1/draw_odd + 1/away_odd) - 1
    return {
        'home': (1/home_odd - total_margin/3) * 100,
        'draw': (1/draw_odd - total_margin/3) * 100,
        'away': (1/away_odd - total_margin/3) * 100
    }
