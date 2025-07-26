#!/bin/bash
COUNTER_FILE="$HOME/FOOTBALL_APP/api_counter.json"
[ ! -f "$COUNTER_FILE" ] && echo "Файл счётчика не найден" && exit 1

CURRENT=$(jq -r '.requests_today' "$COUNTER_FILE")
MAX=$(jq -r '.max_requests' "$COUNTER_FILE")
echo "🔄 Осталось запросов: $((MAX - CURRENT))/$MAX"
