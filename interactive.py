#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import time
from datetime import datetime
import requests
from configparser import ConfigParser

# --- Конфигурация ---
CONFIG_FILE = "configs/api_keys.cfg"
LOG_FILE = "logs/manage.log"
CACHE_FILE = "data/api_cache.json"

# --- Инициализация ---
os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

def log_message(message):
    """Логирование действий"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def load_config():
    """Загрузка API-ключей"""
    config = ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        log_message("ОШИБКА: Файл конфигурации не найден!")
        sys.exit(1)
    config.read(CONFIG_FILE)
    return config

def fetch_fixtures(api_key, league_id):
    """Запрос данных о матчах"""
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?league={league_id}&season=2024"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log_message(f"API Error: {str(e)}")
        return None

def save_cache(data):
    """Кэширование данных"""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def load_cache():
    """Загрузка кэша"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def predict_match(home_team, away_team):
    """Простой алгоритм предсказания"""
    # TODO: Заменить на ML-модель
    return f"Прогноз: {home_team} 2-1 {away_team} (вероятность 65%)"

def main_menu():
    """Главное меню"""
    config = load_config()
    api_key = config.get("API_KEYS", "RAPIDAPI")

    while True:
        print("\n⚽ Football Predictor Pro")
        print("1. Получить текущие матчи")
        print("2. Показать кэшированные данные")
        print("3. Сделать прогноз")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            league_id = input("Введите ID лиги (например, 39 для Premier League): ")
            data = fetch_fixtures(api_key, league_id)
            if data:
                save_cache(data)
                print(json.dumps(data, indent=2, ensure_ascii=False))
        elif choice == "2":
            cached_data = load_cache()
            print(json.dumps(cached_data, indent=2, ensure_ascii=False) if cached_data else "Кэш пуст!")
        elif choice == "3":
            home = input("Хозяева: ")
            away = input("Гости: ")
            print(predict_match(home, away))
        elif choice == "4":
            log_message("Завершение работы")
            sys.exit(0)
        else:
            print("Неверный ввод!")

if __name__ == "__main__":
    log_message("Запуск системы")
    main_menu()
