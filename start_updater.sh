#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/home/storage/shared/FOOTBALL
nohup python -u api/updater.py >> updater.log 2>&1 &
echo "Автообновление запущено. Логи в updater.log"
