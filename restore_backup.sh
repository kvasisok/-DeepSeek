#!/bin/bash

BACKUP_DIR="/storage/emulated/0/FOOTBALL/backups"
DB_PATH="/storage/emulated/0/FOOTBALL/db/football.db"
DATA_DIR="/storage/emulated/0/FOOTBALL/data"

echo "Доступные бэкапы:"
ls -lt $BACKUP_DIR | grep -E 'football_backup_|^total'

read -p "Введите дату бэкапа (формат ГГГГММДД_ЧЧММСС): " backup_date

BACKUP_PREFIX="football_backup_$backup_date"

# Проверяем существование бэкапа
if [ ! -f "$BACKUP_DIR/${BACKUP_PREFIX}.db" ]; then
    echo "Ошибка: бэкап не найден!"
    exit 1
fi

echo "Восстановление из бэкапа $backup_date..."

# 1. Восстанавливаем базу данных
echo "Восстанавливаем БД..."
rm -f $DB_PATH
sqlite3 $DB_PATH ".restore '$BACKUP_DIR/${BACKUP_PREFIX}.db'"

# 2. Восстанавливаем JSON-данные
echo "Восстанавливаем данные API..."
rm -rf $DATA_DIR/*
tar -xzf $BACKUP_DIR/${BACKUP_PREFIX}_data.tar.gz -C $DATA_DIR

# 3. Восстанавливаем скрипты
echo "Восстанавливаем скрипты..."
tar -xzf $BACKUP_DIR/${BACKUP_PREFIX}_scripts.tar.gz -C /storage/emulated/0/FOOTBALL

echo "Восстановление завершено успешно!"
