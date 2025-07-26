#!/bin/bash
CURRENT=$(jq -r '.requests_today' ~/FOOTBALL_APP/api_counter.json)
MAX=$(jq -r '.max_requests' ~/FOOTBALL_APP/api_counter.json)
echo "Осталось запросов: $((MAX - CURRENT))/100"
