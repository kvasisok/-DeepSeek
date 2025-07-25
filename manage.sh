#!/data/data/com.termux/files/usr/bin/bash
echo "$(date +"%Y-%m-%d %H:%M") - API call from $0" >> ~/FOOTBALL_APP/logs/api_usage.log
echo "$(date +"%Y-%m-%d %H:%M") - API call from $0" >> ~/FOOTBALL_APP/logs/api_usage.log
# Полная система управления футбольным анализатором

PROJECT_DIR="$HOME/storage/shared/FOOTBALL"
WEB_DIR="$PROJECT_DIR/web"
DB_FILE="$PROJECT_DIR/db/football.db"

# Цвета
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

show_commands() {
  clear
  echo -e "${GREEN}=== СИСТЕМНЫЕ КОМАНДЫ ===${NC}"
  echo "1. Запустить веб-сервер"
  echo "2. Остановить веб-сервер"
  echo "3. Проверить статус"
  echo "4. Показать логи"
  echo "5. Обновить файлы"
  echo "6. Назад"
}

web_control() {
  while true; do
    show_commands
    read -p "Выберите действие: " choice
    
    case $choice in
      1)
        nohup python "$WEB_DIR/server.py" > "$WEB_DIR/server.log" 2>&1 &
        echo -e "${GREEN}Сервер запущен${NC}"
        sleep 1
        termux-open-url "http://127.0.0.1:8080"
        ;;
      2)
        pkill -f "python server.py"
        echo -e "${YELLOW}Сервер остановлен${NC}"
        sleep 1
        ;;
      3)
        if pgrep -f "python server.py" >/dev/null; then
          echo -e "${GREEN}Статус: Сервер работает${NC}"
        else
          echo -e "${RED}Статус: Сервер не работает${NC}"
        fi
        read -p "Нажмите Enter..."
        ;;
      4)
        clear
        echo -e "${YELLOW}=== ПОСЛЕДНИЕ 10 СТРОК ЛОГОВ ===${NC}"
        tail -n 10 "$WEB_DIR/server.log"
        read -p "Нажмите Enter..."
        ;;
      5)
        update_files_menu
        ;;
      6)
        return
        ;;
      *)
        echo -e "${RED}Неверный выбор!${NC}"
        sleep 1
        ;;
    esac
  done
}

update_files_menu() {
  while true; do
    clear
    echo -e "${GREEN}=== ОБНОВЛЕНИЕ ФАЙЛОВ ===${NC}"
    echo "1. Обновить server.py"
    echo "2. Обновить index.html"
    echo "3. Обновить app.js"
    echo "4. Назад"
    
    read -p "Выберите файл: " choice
    case $choice in
      1)
        update_file "server.py" "$WEB_DIR/server.py"
        ;;
      2)
        update_file "index.html" "$WEB_DIR/templates/index.html"
        ;;
      3)
        update_file "app.js" "$WEB_DIR/static/js/app.js"
        ;;
      4)
        return
        ;;
      *)
        echo -e "${RED}Неверный выбор!${NC}"
        sleep 1
        ;;
    esac
  done
}

update_file() {
  file_name=$1
  file_path=$2
  
  echo -e "\n${YELLOW}=== ТЕКУЩЕЕ СОДЕРЖАНИЕ $file_name ===${NC}"
  cat "$file_path" 2>/dev/null || echo "Файл не существует"
  
  echo -e "\n${YELLOW}Введите новое содержимое (Ctrl+D для сохранения):${NC}"
  echo "----------------------------------------"
  cat > "$file_path"
  echo -e "${GREEN}Файл $file_name обновлен!${NC}"
  sleep 1
}

main_menu() {
  while true; do
    clear
    echo -e "${GREEN}=== ФУТБОЛЬНЫЙ АНАЛИЗАТОР ===${NC}"
    echo "1. Управление веб-интерфейсом"
    echo "2. Запустить консольный интерфейс"
    echo "3. Обновить данные (парсинг)"
    echo "4. Создать бэкап"
    echo "5. Выход"
    
    read -p "Выберите пункт: " choice
    case $choice in
      1) web_control ;;
      2) bash "$PROJECT_DIR/football_cli.sh" ;;
      3) bash "$PROJECT_DIR/update_all.sh" ;;
      4) bash "$PROJECT_DIR/backup_manager.sh" ;;
      5) exit 0 ;;
      *) echo -e "${RED}Неверный выбор!${NC}"; sleep 1 ;;
    esac
  done
}

main_menu
