from parsers.optimized_odds import OptimizedOddsAnalyzer
from parsers.fbref_parser import parse_fbref
import plotly.express as px

def create_plots(report):
    """Создание графиков через Plotly"""
    try:
        # График ударов
        fig = px.bar(
            x=['Все удары', 'Удары в створ'],
            y=[report['shots'], report['shots_on_target']],
            title=f'Статистика ударов (Точность: {report["shots_on_target"]/report["shots"]:.0%})',
            labels={'y': 'Количество'},
            color=['Все удары', 'Удары в створ'],
            color_discrete_sequence=['#636EFA', '#00CC96']
        )
        fig.write_html("/sdcard/Download/fb_shots.html")
        
        # График эффективности вратаря
        fig = px.pie(
            values=[report['gk_save_percent'], 100-report['gk_save_percent']],
            names=['Сейвы', 'Пропущенные'],
            title=f'Эффективность вратаря: {report["gk_save_percent"]}%'
        )
        fig.write_html("/sdcard/Download/fb_gk.html")
        
        print("\n✅ Графики сохранены в /sdcard/Download/")
        print("fb_shots.html и fb_gk.html")
        
    except Exception as e:
        print(f"⚠️ Ошибка визуализации: {str(e)[:50]}")

def main():
    print("🔍 Анализ футбольного матча...")
    
    # Получаем данные
    stats = parse_fbref("https://fbref.com/en/matches/sample-url")
    
    # Анализ коэффициентов
    analyzer = OptimizedOddsAnalyzer()
    odds = analyzer.get_odds(1369607)  # test fixture ID
    
    # Вывод результатов
    print(f"\n📊 Статистика:")
    print(f"Удары: {stats['shots']} (В створ: {stats['shots_on_target']})")
    print(f"% сейвов: {stats['gk_save_percent']}%")
    
    if odds:
        print("\n🎲 Лучшие коэффициенты:")
        for bet_type, values in odds.items():
            best = max(values['values'], key=lambda x: x['odd'])
            print(f"{bet_type}: {best['value']} @ {best['odd']:.2f}")
    
    create_plots(stats)

if __name__ == "__main__":
    main()
