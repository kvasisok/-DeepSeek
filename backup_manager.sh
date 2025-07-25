#!/bin/bash

# Используем внутреннее хранилище Termux
TERMUX_STORAGE="$HOME/storage/shared"
BACKUP_DIR="$TERMUX_STORAGE/FOOTBALL/backups"
DB_PATH="$TERMUX_STORAGE/FOOTBALL/db/football.db"
DATA_DIR="$TERMUX_STORAGE/FOOTBALL/data"
LOG_FILE="$BACKUP_DIR/backup.log"
RETENTION_DAYS=30

# Создаем папки, если их нет
mkdir -p "$BACKUP_DIR" 2>/dev/null || {
    echo "Ошибка: Не могу создать папку $BACKUP_DIR"
    exit 1
}

# Функция логирования
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=== Начало создания бэкапа ==="

# 1. Бэкап базы данных
log "1/3 Создание бэкапа БД..."
if ! sqlite3 "$DB_PATH" ".backup '$BACKUP_DIR/football_backup_$(date +%Y%m%d_%H%M%S).db'"; then
    log "Ошибка: Не удалось создать бэкап БД"
    exit 1
fi

# 2. Бэкап данных
log "2/3 Архивирование данных API..."
if ! tar -czf "$BACKUP_DIR/football_backup_$(date +%Y%m%d_%H%M%S)_data.tar.gz" -C "$DATA_DIR" .; then
    log "Ошибка: Не удалось архивировать данные"
    exit 1
fi

# 3. Бэкап скриптов
log "3/3 Архивирование скриптов..."
if ! tar -czf "$BACKUP_DIR/football_backup_$(date +%Y%m%d_%H%M%S)_scripts.tar.gz" \
    -C "$TERMUX_STORAGE/FOOTBALL" \
    api/ analysis/ utils/; then
    log "Ошибка: Не удалось архивировать скрипты"
    exit 1
fi

# 4. Очистка старых бэкапов
log "Очистка старых бэкапов (>$RETENTION_DAYS дней)..."
find "$BACKUP_DIR" -name "football_backup_*" -type f -mtime +$RETENTION_DAYS -print -delete | while read -r file; do
    log "Удален: $file"
done

log "=== Бэкап успешно создан ==="
