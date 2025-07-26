#!/bin/bash
CONFIG_FILE="$HOME/FOOTBALL_APP/api_counter.json"
TODAY=$(date +%Y-%m-%d)

# Создаём файл если отсутствует
if [ ! -f "$CONFIG_FILE" ]; then
    echo '{"last_reset":"'"$TODAY"'","requests_today":0,"max_requests":100}' > "$CONFIG_FILE"
fi

# Функция безопасного обновления
update_counter() {
    jq \
    --arg today "$TODAY" \
    --argjson req "$1" \
    '.last_reset = $today | .requests_today = $req' \
    "$CONFIG_FILE" > tmp.json && mv tmp.json "$CONFIG_FILE"
}

# Проверяем валидность JSON
if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
    echo "⚠️ Ошибка в конфиге! Создаём новый..."
    echo '{"last_reset":"'"$TODAY"'","requests_today":0,"max_requests":100}' > "$CONFIG_FILE"
fi

# Проверка сброса
LAST_RESET=$(jq -r '.last_reset' "$CONFIG_FILE")
if [ "$LAST_RESET" != "$TODAY" ]; then
    update_counter 0
fi

# Проверка лимита
CURRENT=$(jq -r '.requests_today' "$CONFIG_FILE")
MAX=$(jq -r '.max_requests' "$CONFIG_FILE")

if [ "$CURRENT" -ge "$MAX" ]; then
    echo "⚠️ Лимит исчерпан (100/день). Ждите 00:00 UTC."
    exit 1
fi

# Увеличиваем счётчик
update_counter $((CURRENT + 1))
