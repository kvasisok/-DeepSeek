#!/data/data/com.termux/files/usr/bin/bash
# Меню прогнозов

PROJECT_DIR="$HOME/storage/shared/FOOTBALL"
DB="$PROJECT_DIR/db/football.db"
match_id=$1

while true; do
    clear
    match_info=$(sqlite3 "$DB" <<END
        SELECT 
            (SELECT name FROM teams WHERE id = home_team_id) || ' vs ' || 
            (SELECT name FROM teams WHERE id = away_team_id),
            utc_date
        FROM matches WHERE id = $match_id;
END
    )
    
    echo "Матч: $match_info"
    echo "1. Сделать прогноз"
    echo "2. Посмотреть существующий прогноз"
    echo "3. Обновить прогноз"
    echo "4. Назад"
    read -p "Выберите действие: " choice
    
    case $choice in
        1) make_prediction "$match_id" ;;
        2) view_prediction "$match_id" ;;
        3) update_prediction "$match_id" ;;
        4) break ;;
        *) echo "Неверный выбор!"; sleep 1 ;;
    esac
    read -p "Нажмите Enter чтобы продолжить..."
done

make_prediction() {
    echo "Генерация прогноза для матча ID: $1..."
    # Здесь будет логика прогнозирования
    read -p "Введите предполагаемый счет (например, 2-1): " score
    sqlite3 "$DB" "INSERT OR REPLACE INTO predictions VALUES ($1, '$score', strftime('%s', 'now'));"
    echo "Прогноз сохранен!"
}

view_prediction() {
    prediction=$(sqlite3 "$DB" "SELECT prediction FROM predictions WHERE match_id = $1;")
    if [ -z "$prediction" ]; then
        echo "Прогноз отсутствует!"
    else
        echo "Текущий прогноз: $prediction"
    fi
}

update_prediction() {
    make_prediction "$1"
}
