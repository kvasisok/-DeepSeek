import csv
from pathlib import Path
from utils.add_odds import update_odds
from utils.logger import log
from datetime import datetime

def clear_screen():
    print("\033[H\033[J")  # ANSI escape codes для очистки экрана

def show_odds():
    db_path = Path(__file__).parent / 'db' / 'odds.csv'
    if not db_path.exists():
        print("База коэффициентов пуста")
        return
    
    with open(db_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        print("\nТекущие коэффициенты:")
        print("{:<12} {:<15} {:<15} {:<6} {:<6} {:<6} {:<16}".format(*header))
        for row in reader:
            if row:  # Пропускаем пустые строки
                print("{:<12} {:<15} {:<15} {:<6} {:<6} {:<6} {:<16}".format(*row))

def add_match_manual():
    print("\nДобавление нового матча:")
    match_id = input("ID матча: ").strip()
    home = input("Команда хозяев: ").strip()
    away = input("Команда гостей: ").strip()
    
    try:
        h_odd = float(input("Коэф. на хозяев: "))
        d_odd = float(input("Коэф. на ничью: "))
        a_odd = float(input("Коэф. на гостей: "))
        
        update_odds(match_id, home, away, h_odd, d_odd, a_odd)
        log('MANUAL_ADD', f'Added {home} vs {away}')
        print("Матч успешно добавлен!")
    except ValueError as e:
        print(f"Ошибка: {e}")

def show_logs():
    log_path = Path(__file__).parent / 'logs' / 'app.log'
    if not log_path.exists():
        print("Логи отсутствуют")
        return
    
    with open(log_path, 'r') as f:
        print("\nПоследние события:")
        print(f.read())

def main_menu():
    while True:
        clear_screen()
        print("=== Football Analyzer ===")
        print("1. Показать текущие коэффициенты")
        print("2. Добавить/обновить матч")
        print("3. Показать логи операций")
        print("4. Выход")
        
        choice = input("Выберите пункт: ").strip()
        
        if choice == "1":
            show_odds()
        elif choice == "2":
            add_match_manual()
        elif choice == "3":
            show_logs()
        elif choice == "4":
            print("Выход из программы")
            break
        else:
            print("Некорректный выбор")
        
        input("\nНажмите Enter чтобы продолжить...")

if __name__ == "__main__":
    main_menu()
