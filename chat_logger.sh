#!/bin/bash
LOG_FILE="chat_logs/chat_$(date +%Y%m%d_%H%M%S).log"
echo -e "=== USER ===\n$1\n=== ASSISTANT ===\n$2" > $LOG_FILE
git add $LOG_FILE
git commit -m "Auto: chat log $(date +'%d.%m.%Y %H:%M')" >/dev/null
