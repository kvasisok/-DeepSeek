#!/data/data/com.termux/files/usr/bin/bash
# Поиск команды

PROJECT_DIR="$HOME/storage/shared/FOOTBALL"
DB="$PROJECT_DIR/db/football.db"

search_team() {
    read -p "Введите название команды: " team_name
    results=$(sqlite3 "$DB" <<END
        SELECT id, name FROM teams 
        WHERE name LIKE '%$team_name%'
        LIMIT 5;
END
    )
    
    if [ -z "$results" ]; then
        echo "Команда не найдена!"
        return
    fi
    
    echo "Найденные команды:"
    i=1
    declare -A teams
    while IFS='|' read -r id name; do
        echo "$i. $name (ID: $id)"
        teams[$i]=$id
        ((i++))
    done <<< "$results"
    
    read -p "Выберите команду (1-$((i-1))): " num
    selected_id=${teams[$num]}
    
    if [ -z "$selected_id" ]; then
        echo "Неверный выбор!"
        return
    fi
    
    # Меню действий с командой
    while true; do
        clear
        team_name=$(sqlite3 "$DB" "SELECT name FROM teams WHERE id = $selected_id;")
        echo "Команда: $team_name"
        echo "1. Последние 5 матчей"
        echo "2. Ближайшие 5 матчей"
        echo "3. Общая статистика"
        echo "4. Назад"
        read -p "Выберите действие: " action
        
        case $action in
            1) show_matches "$selected_id" "past" ;;
            2) show_matches "$selected_id" "future" ;;
            3) show_stats "$selected_id" ;;
            4) break ;;
            *) echo "Неверный выбор!"; sleep 1 ;;
        esac
        read -p "Нажмите Enter чтобы продолжить..."
    done
}

show_matches() {
    team_id=$1
    type=$2
    
    if [ "$type" = "past" ]; then
        query="SELECT m.id, m.utc_date, 
               (SELECT name FROM teams WHERE id = m.home_team_id) || ' vs ' || 
               (SELECT name FROM teams WHERE id = m.away_team_id),
               m.home_score || '-' || m.away_score
               FROM matches m 
               WHERE (home_team_id = $team_id OR away_team_id = $team_id)
               AND status = 'FINISHED'
               ORDER BY utc_date DESC LIMIT 5;"
    else
        query="SELECT m.id, m.utc_date, 
               (SELECT name FROM teams WHERE id = m.home_team_id) || ' vs ' || 
               (SELECT name FROM teams WHERE id = m.away_team_id)
               FROM matches m 
               WHERE (home_team_id = $team_id OR away_team_id = $team_id)
               AND status = 'SCHEDULED'
               ORDER BY utc_date ASC LIMIT 5;"
    fi
    
    matches=$(sqlite3 "$DB" "$query")
    
    echo ""
    echo "Матчи:"
    i=1
    declare -A match_ids
    while IFS='|' read -r id date teams score; do
        echo "$i. $teams ($date) $score"
        match_ids[$i]=$id
        ((i++))
    done <<< "$matches"
    
    if [ "$type" = "future" ]; then
        read -p "Выберите матч (1-$((i-1))) для прогноза: " match_num
        selected_match=${match_ids[$match_num]}
        if [ -n "$selected_match" ]; then
            bash "$PROJECT_DIR/predict_menu.sh" "$selected_match"
        fi
    fi
}

show_stats() {
    team_id=$1
    echo ""
    echo "=== Статистика команды ==="
    sqlite3 "$DB" <<END
        SELECT 
            (SELECT COUNT(*) FROM matches WHERE home_team_id = $team_id OR away_team_id = $team_id) as total_matches,
            (SELECT COUNT(*) FROM matches WHERE (home_team_id = $team_id AND home_score > away_score) OR 
                                              (away_team_id = $team_id AND away_score > home_score)) as wins,
            (SELECT COUNT(*) FROM matches WHERE home_team_id = $team_id OR away_team_id = $team_id) as draws;
END
}

# Запуск поиска
search_team
