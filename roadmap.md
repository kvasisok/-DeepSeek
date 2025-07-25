# Football Predictor Roadmap (Termux Edition)

## Технические стандарты
1. Все файлы создаются через `cat > path/file.ext <<'EOF'` 
2. Изменения в файлах вносятся:
   - Через `sed -i` для простых правок
   - Полной перезаписью для сложных изменений
3. Коды для Termux даются явно с проверками

## Этапы выполнения

### 1. Исторические данные (3 дня)
```bash
# Создаем парсер
cat > /storage/emulated/0/Documents/FOOTBALL_APP/parsers/history_parser.py <<'EOF'
import requests
from datetime import datetime

def fetch_history(team_id):
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit=10"
    response = requests.get(url, headers={"X-Auth-Token": "005b8a3887ac4870920d909a7e31c7c5"})
    return [match for match in response.json()['matches'] 
            if datetime.fromisoformat(match['utcDate']) > datetime(2023,1,1)]
