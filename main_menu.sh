#!/data/data/com.termux/files/usr/bin/bash
# Главное меню

PROJECT_DIR="$HOME/storage/shared/FOOTBALL"

while true; do
    clear
    echo "=== ГЛАВНОЕ МЕНЮ ==="
    echo "1. Управление данными"
    echo "2. Поиск команды"
    echo "3. Прогнозы матчей"
    echo "4. Выход"
    read -p "Выберите пункт: " choice

    case $choice in
        1) bash "$PROJECT_DIR/data_menu.sh" ;;
        2) bash "$PROJECT_DIR/search_menu.sh" ;;
        3) bash "$PROJECT_DIR/predict_menu.sh" ;;
        4) exit 0 ;;
        *) echo "Неверный выбор!"; sleep 1 ;;
    esac
done
