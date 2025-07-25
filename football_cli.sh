#!/data/data/com.termux/files/usr/bin/bash
# Улучшенное меню с визуальным откликом

DB="$HOME/storage/shared/FOOTBALL/db/football.db"
LOG_FILE="$HOME/storage/shared/FOOTBALL/cli.log"

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Логирование
log() {
  echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Функция вывода сообщения
message() {
  clear
  echo -e "${YELLOW}$1${NC}"
  sleep 1
}

search_team() {
  read -p "Введите название команды: " team
  result=$(sqlite3 "$DB" <<SQL
    SELECT id, name FROM teams 
    WHERE name LIKE '%$team%' 
    LIMIT 5;
SQL
)
  
  if [ -z "$result" ]; then
    message "${RED}Команда '$team' не найдена${NC}"
    return
  fi

  echo -e "${GREEN}Найденные команды:${NC}"
  i=1
  declare -A teams
  while IFS='|' read -r id name; do
    echo "$i. $name"
    teams[$i]=$id
    ((i++))
  done <<< "$result"

  read -p "Выберите команду (1-$((i-1)) или 0 для отмены: " num
  
  if [ "$num" -eq 0 ]; then
    return
  elif [ -z "${teams[$num]}" ]; then
    message "${RED}Неверный выбор!${NC}"
  else
    team_menu "${teams[$num]}"
  fi
}

show_matches() {
  clear
  if [ "$2" = "past" ]; then
    query="SELECT m.id, m.utc_date, 
           t1.short_name, m.home_score, 
           t2.short_name, m.away_score 
           FROM matches m
           JOIN teams t1 ON m.home_team_id = t1.id
           JOIN teams t2 ON m.away_team_id = t2.id
           WHERE (m.home_team_id = $1 OR m.away_team_id = $1) 
           AND m.status = 'FINISHED'
           ORDER BY m.utc_date DESC LIMIT 5;"
    title="${GREEN}Последние 5 матчей:${NC}"
  else
    query="SELECT m.id, m.utc_date, 
           t1.short_name, t2.short_name
           FROM matches m
           JOIN teams t1 ON m.home_team_id = t1.id
           JOIN teams t2 ON m.away_team_id = t2.id
           WHERE (m.home_team_id = $1 OR m.away_team_id = $1) 
           AND m.status = 'SCHEDULED'
           ORDER BY m.utc_date ASC LIMIT 5;"
    title="${GREEN}Ближайшие 5 матчей:${NC}"
  fi

  echo -e "$title"
  results=$(sqlite3 "$DB" "$query")
  
  if [ -z "$results" ]; then
    message "${RED}Матчи не найдены${NC}"
    return
  fi

  while IFS='|' read -r id date t1 score1 t2 score2; do
    if [ "$2" = "past" ]; then
      echo "$date | $t1 $score1:$score2 $t2 (ID: $id)"
    else
      echo "$date | $t1 vs $t2 (ID: $id)"
    fi
  done <<< "$results"

  if [ "$2" = "future" ]; then
    echo -e "\n${YELLOW}Действия:${NC}"
    read -p "Введите ID матча для прогноза (или 0 для отмены): " match_id
    if [ "$match_id" -ne 0 ]; then
      match_menu "$match_id"
    fi
  else
    read -p "Нажмите Enter чтобы продолжить..."
  fi
}

# Главное меню
main_menu() {
  while true; do
    clear
    echo -e "${GREEN}=== Футбольный анализатор ===${NC}"
    echo "1. Поиск команды"
    echo "2. Обновить все данные"
    echo "3. Управление бэкапами"
    echo -e "${RED}4. Выход${NC}"
    
    read -p "Выберите пункт: " choice
    case $choice in
      1) search_team ;;
      2) 
        message "Запуск обновления данных..."
        bash ~/storage/shared/FOOTBALL/update_all.sh && \
          message "${GREEN}Данные успешно обновлены${NC}" || \
          message "${RED}Ошибка при обновлении${NC}"
        ;;
      3) 
        message "Создание бэкапа..."
        bash ~/storage/shared/FOOTBALL/backup_manager.sh && \
          message "${GREEN}Бэкап успешно создан${NC}" || \
          message "${RED}Ошибка при создании бэкапа${NC}"
        ;;
      4) exit 0 ;;
      *) message "${RED}Неверный выбор!${NC}" ;;
    esac
  done
}

main_menu
