#!/data/data/com.termux/files/usr/bin/bash

# Пути для логов
LOG_FILE="$HOME/storage/shared/FOOTBALL/update.log"
ERROR_LOG="$HOME/storage/shared/FOOTBALL/error.log"

# Очищаем логи предыдущих запусков
> "$LOG_FILE"
> "$ERROR_LOG"

{
    echo "=== Запуск обновления $(date) ==="
    
    # 1. Обновление данных команд
    echo "Запуск reliable_parser.py..."
    cd "$HOME/storage/shared/FOOTBALL"
    python3 api/reliable_parser.py --full-update
    
    # 2. Обновление погодных данных
    echo "Запуск weather_api_parser.py..."
    python3 api/weather_api_parser.py --update-pending
    
    # 3. Создание бэкапа
    echo "Запуск backup_manager.sh..."
    bash backup_manager.sh
    
    echo "=== Обновление завершено $(date) ==="

} > "$LOG_FILE" 2> "$ERROR_LOG"

# Обработка ошибок
if [ -s "$ERROR_LOG" ]; then
    echo -e "\n=== ОШИБКИ ===" >> "$LOG_FILE"
    cat "$ERROR_LOG" >> "$LOG_FILE"
    
    # Отправка уведомления в Termux
    if command -v termux-notification &> /dev/null; then
        error_msg=$(head -n 3 "$ERROR_LOG")
        termux-notification --title "Ошибка Football API" --content "$error_msg"
    fi
fi
# Очищаем пустой error.log (если нет ошибок)
[ ! -s "$ERROR_LOG" ] && rm "$ERROR_LOG"
# Обновление новых данных
python3 api/player_stats_updater.py
python3 api/odds_parser.py
