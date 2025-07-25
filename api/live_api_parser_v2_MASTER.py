import requests
import json
from datetime import datetime
import time
import os

# Конфигурация
API_KEY = "005b8a3887ac4870920d909a7e31c7c5"
BASE_URL = "http://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}
REQUEST_DELAY = 6.1  # 10 запросов в минуту (60/10 + буфер)
DATA_DIR = "/storage/emulated/0/FOOTBALL/data/raw"

def init_data_dir():
    """Создает папки для данных, если их нет"""
    os.makedirs(DATA_DIR, exist_ok=True)

def save_data(data, filename):
    """Сохраняет данные в JSON с датой обновления"""
    data["last_updated"] = datetime.now().isoformat()
    with open(f"{DATA_DIR}/{filename}", "w") as f:
        json.dump(data, f, indent=2)

def make_request(url):
    """Безопасный запрос с задержкой и обработкой лимитов"""
    time.sleep(REQUEST_DELAY)
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            retry_after = int(e.response.headers.get("Retry-After", 60))
            print(f"Лимит! Ждем {retry_after} сек...")
            time.sleep(retry_after)
            return make_request(url)
        print(f"Ошибка {e.response.status_code}: {url}")
        return None

def get_available_leagues():
    """Получает список доступных лиг"""
    url = f"{BASE_URL}/competitions"
    response = make_request(url)
    if response:
        leagues = {comp["code"]: comp["name"] for comp in response.json()["competitions"] if comp["code"]}
        save_data({"leagues": leagues}, "leagues.json")
        return leagues
    return {}

def get_league_matches(league_code):
    """Парсит матчи конкретной лиги"""
    url = f"{BASE_URL}/competitions/{league_code}/matches"
    response = make_request(url)
    if response:
        matches = response.json()["matches"]
        save_data({"matches": matches}, f"matches_{league_code}.json")
        return matches
    return []

def main():
    init_data_dir()
    
    # 1. Получаем актуальные лиги
    print("Получение списка лиг...")
    leagues = get_available_leagues()
    if not leagues:
        print("Не удалось загрузить лиги. Проверьте API_KEY.")
        return

    # 2. Парсим матчи для каждой лиги
    total_matches = 0
    for code, name in leagues.items():
        print(f"Обработка лиги: {name} ({code})")
        matches = get_league_matches(code)
        total_matches += len(matches)
    
    print(f"Готово! Обработано лиг: {len(leagues)}, матчей: {total_matches}")

if __name__ == "__main__":
    main()
