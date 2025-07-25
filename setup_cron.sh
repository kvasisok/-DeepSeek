#!/bin/bash

# Устанавливаем cron для ежедневных бэкапов в 3:00
(crontab -l 2>/dev/null; echo "0 3 * * * /storage/emulated/0/FOOTBALL/backup_manager.sh") | crontab -

echo "Ежедневные бэкапы настроены (в 3:00)"
