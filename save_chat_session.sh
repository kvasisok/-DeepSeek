#!/bin/bash

# Полный путь к папке проекта
PROJECT_DIR="$HOME/FOOTBALL_APP"

# Создаем папку для логов
mkdir -p "$PROJECT_DIR/chat_logs"

# Создаем временные файлы, если их нет
touch "$PROJECT_DIR/last_user_input.txt"
touch "$PROJECT_DIR/last_bot_response.txt"

# Формируем имя файла лога
LOG_FILE="$PROJECT_DIR/chat_logs/session_$(date +%Y%m%d_%H%M%S).log"

# Записываем данные в лог
{
    echo "=== CHAT SESSION $(date +'%Y-%m-%d %H:%M:%S') ==="
    echo "USER: $(cat "$PROJECT_DIR/last_user_input.txt" 2>/dev/null || echo 'No input')"
    echo "ASSISTANT: $(cat "$PROJECT_DIR/last_bot_response.txt" 2>/dev/null || echo 'No response')"
} > "$LOG_FILE"

# Обновляем файл памяти (если существует)
MEMORY_FILE="$PROJECT_DIR/ДиСи_моя_память.txt"
if [ -f "$MEMORY_FILE" ]; then
    echo -e "\n[Обновлено: $(date +'%Y-%m-%d %H:%M')]" >> "$MEMORY_FILE"
fi

# Git операции (только если это git-репозиторий)
if [ -d "$PROJECT_DIR/.git" ]; then
    cd "$PROJECT_DIR" || exit 1
    git add --all
    git commit -m "Chat backup $(date +'%d.%m.%Y %H:%M')" >/dev/null
    git push origin main >/dev/null 2>&1
fi

echo "✅ Чат сохранен в: $LOG_FILE"
