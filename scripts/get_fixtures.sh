#!/bin/bash
source ~/FOOTBALL_APP/scripts/api_utils.sh || exit 1

curl -s -X GET \
  -H "X-RapidAPI-Key: $(grep RAPIDAPI_KEY ~/FOOTBALL_APP/.env | cut -d= -f2)" \
  -H "X-RapidAPI-Host: api-football-v1.p.rapidapi.com" \
  "https://api-football-v1.p.rapidapi.com/v2/fixtures?league=39&season=2023&next=5" \
  > ~/FOOTBALL_APP/data/latest_fixtures.json

echo "✅ Фикстуры сохранены. Использовано: $(jq -r '.requests_today' ~/FOOTBALL_APP/api_counter.json)/100"
