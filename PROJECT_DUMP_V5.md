# ⚽ Football Predictor Pro - Полный дамп проекта
## Версия 5.0 (Termux Optimized)
## Дата создания: $(date +"%Y-%m-%d %H:%M")

### 📂 Структура проекта
```bash
    Termux_basic_commands.md
    Termux_basic_commands.txt
    __pycache__
    analysis
    api
    api_key.txt
    backup_manager.sh
    backups
    configs
    data
    db
    fix_permissions.sh
    football_cli.sh
    interactive.py
    leagues.json
    live_api_parser_v2.py
    logs
    main_menu.sh
    manage.log
    manage.sh
    menu.py
    odds.json
    parsers
    predict_menu.sh
    project_plan.txt
    restore_backup.sh
    roadmap.md
    roadmap1.md
    run_parsers.sh
    search_menu.sh
    setup_cron.sh
    start_updater.sh
    templates
    test_data.json
    test_file.txt
    update.log
    update_all.sh
    update_all.sh.backup
    update_all.sh.bak
    update_teams.log
    updater.log
    utils
    venv
    web
    
    interactive.cpython-312.pyc
    
    basic_stats.py
    
    __pycache__
    db_handler.py
    football_data.py
    football_data_loader.py
    football_parser.py
    geocoder.py
    live_api_parser_v2.py
    live_api_parser_v2_BACKUP.py
    live_api_parser_v2_MASTER.py
    main_parser.py
    match_updater.py
    odds_parser.py
    player_stats_updater.py
    reliable_parser.py
    safe_parser.py
    safe_parser_v3.py
    simple_parser.py
    static_data_saver.py
    static_data_saver_v2.py
    team_details_updater.py
    team_updater_pro.py
    temp_parser.py
    transfermarkt_parser.py
    ultimate_parser.py
    updater.py
    weather_api_parser.py
    weather_parser.py
    weather_parser_current.py
    
    db_handler.cpython-312.pyc
    football_data_loader.cpython-312.pyc
    transfermarkt_parser.cpython-312.pyc
    
    backup.log
    backup_20250719_2246.tar.gz
    football_app_20250719_2239.tar.gz
    football_app_backup_20250719_2114.tar.gz
    football_app_backup_20250719_2115.tar.gz
    football_app_backup_20250719_2125.tar.gz
    football_backup_20250718_120818.db
    football_backup_20250718_120818_data.tar.gz
    football_backup_20250718_120818_scripts.tar.gz
    football_backup_20250718_124648.db
    football_backup_20250718_124648_data.tar.gz
    football_backup_20250718_124648_scripts.tar.gz
    football_backup_20250718_124815.db
    football_backup_20250718_124815_data.tar.gz
    football_backup_20250718_124815_scripts.tar.gz
    football_backup_20250718_130536.db
    football_backup_20250718_130536_data.tar.gz
    football_backup_20250718_130536_scripts.tar.gz
    football_backup_20250718_141640.db
    football_backup_20250718_141640_data.tar.gz
    football_backup_20250718_141640_scripts.tar.gz
    football_backup_20250718_161846.db
    football_backup_20250718_161846_data.tar.gz
    football_backup_20250718_161846_scripts.tar.gz
    football_backup_20250718_161847.db
    football_backup_20250718_161847_data.tar.gz
    football_backup_20250718_161847_scripts.tar.gz
    football_backup_20250718_162037.db
    football_backup_20250718_162037_data.tar.gz
    football_backup_20250718_162037_scripts.tar.gz
    football_backup_20250718_165657.db
    football_backup_20250718_165657_data.tar.gz
    football_backup_20250718_165657_scripts.tar.gz
    football_backup_20250718_165707.db
    football_backup_20250718_165707_data.tar.gz
    football_backup_20250718_165707_scripts.tar.gz
    football_backup_20250718_171337.db
    football_backup_20250718_171337_data.tar.gz
    football_backup_20250718_171337_scripts.tar.gz
    football_backup_20250718_171345.db
    football_backup_20250718_171345_data.tar.gz
    football_backup_20250718_171345_scripts.tar.gz
    football_backup_20250718_171355.db
    football_backup_20250718_171355_data.tar.gz
    football_backup_20250718_171355_scripts.tar.gz
    football_backup_20250718_180054.db
    football_backup_20250718_180055_data.tar.gz
    football_backup_20250718_180055_scripts.tar.gz
    football_backup_20250718_182357.db
    football_backup_20250718_182357_data.tar.gz
    football_backup_20250718_182357_scripts.tar.gz
    football_backup_20250718_191944.db
    football_backup_20250718_191944_data.tar.gz
    football_backup_20250718_191944_scripts.tar.gz
    football_backup_20250718_192009.db
    football_backup_20250718_192009_data.tar.gz
    football_backup_20250718_192009_scripts.tar.gz
    football_backup_20250719_000002.db
    football_backup_20250719_000002_data.tar.gz
    football_backup_20250719_000002_scripts.tar.gz
    football_backup_20250719_060002.db
    football_backup_20250719_060002_data.tar.gz
    football_backup_20250719_060003_scripts.tar.gz
    
    api_config.json
    
    processed
    raw
    
    
    leagues.json
    matches_BL1.json
    matches_BSA.json
    matches_CL.json
    matches_CLI.json
    matches_DED.json
    matches_EC.json
    matches_ELC.json
    matches_FL1.json
    matches_PD.json
    matches_PL.json
    matches_PPL.json
    matches_SA.json
    matches_WC.json
    
    football.db
    matches.csv
    matches_cache.json
    odds.csv
    predictions
    schema.sql
    stats.csv
    
    
    app.log
    manage.log
    weather_parser.log
    
    __pycache__
    flashscore_parser.py
    history_parser.py
    local_odds.py
    odds_api.py
    odds_parser.py
    team_ids.json
    transfermarkt_parser.py
    
    flashscore_parser.cpython-312.pyc
    history_parser.cpython-312.pyc
    local_odds.cpython-312.pyc
    odds_fallback.cpython-312.pyc
    odds_parser.cpython-312.pyc
    transfermarkt_parser.cpython-312.pyc
    
    
    __init__.py
    __pycache__
    add_odds.py
    archive.py
    colors.py
    db_connector.py
    db_operations.py
    logger.py
    predict.py
    report.py
    search.py
    
    __init__.cpython-312.pyc
    add_odds.cpython-312.pyc
    archive.cpython-312.pyc
    colors.cpython-312.pyc
    db_connector.cpython-312.pyc
    db_operations.cpython-312.pyc
    logger.cpython-312.pyc
    predict.cpython-312.pyc
    report.cpython-312.pyc
    search.cpython-312.pyc
    
    include
    lib
    
    python3.12
    
    
    python3.12
    
    site-packages
    
    
    css
    js
    server.log
    server.py
    static
    templates
    
    
    
    js
    
    
    index.html
```

### 🔧 Технические данные
```bash
Termux Variables:
TERMUX_API_VERSION=0.52.0
TERMUX_APK_RELEASE=F_DROID
TERMUX_APP_PACKAGE_MANAGER=apt
TERMUX_APP_PID=8327
TERMUX_APP__DATA_DIR=/data/user/0/com.termux
TERMUX_APP__LEGACY_DATA_DIR=/data/data/com.termux
TERMUX_APP__SE_FILE_CONTEXT=u:object_r:app_data_file:s0:c5,c259,c512,c768
TERMUX_APP__SE_INFO=default:targetSdkVersion=28:complete
TERMUX_IS_DEBUGGABLE_BUILD=0
TERMUX_MAIN_PACKAGE_FORMAT=debian
TERMUX_VERSION=0.118.3
TERMUX__HOME=/data/data/com.termux/files/home
TERMUX__PREFIX=/data/data/com.termux/files/usr
TERMUX__ROOTFS_DIR=/data/data/com.termux/files
TERMUX__SE_PROCESS_CONTEXT=u:r:untrusted_app_27:s0:c5,c259,c512,c768
TERMUX__USER_ID=0
Packages CPU architecture:
aarch64
Subscribed repositories:
# sources.list
deb https://packages-cf.termux.dev/apt/termux-main stable main
Updatable packages:
openjdk-17-x/stable 17.0.16-2 aarch64 [upgradable from: 17.0.16-1]
openjdk-17/stable 17.0.16-2 aarch64 [upgradable from: 17.0.16-1]
openjdk-21-x/stable 21.0.8-1 aarch64 [upgradable from: 21.0.8]
openjdk-21/stable 21.0.8-1 aarch64 [upgradable from: 21.0.8]
termux-tools version:
1.45.0
Android version:
15
Kernel build information:
Linux localhost 5.4.242-30958140-abG996NKSS9HYE5 #1 SMP PREEMPT Wed May 21 09:56:38 KST 2025 aarch64 Android
Device manufacturer:
samsung
Device model:
SM-G996N
Supported ABIs:
SUPPORTED_ABIS: arm64-v8a,armeabi-v7a,armeabi
SUPPORTED_32_BIT_ABIS: armeabi-v7a,armeabi
SUPPORTED_64_BIT_ABIS: arm64-v8a
LD Variables:
LD_LIBRARY_PATH=
LD_PRELOAD=/data/data/com.termux/files/usr/lib/libtermux-exec-ld-preload.so
Installed termux plugins:
com.termux.widget versionCode:1000
com.termux.api versionCode:1001
```

### 🔧 Технические данные окружения
```bash
Termux Variables:
TERMUX_API_VERSION=0.52.0
TERMUX_APK_RELEASE=F_DROID
TERMUX_APP_PACKAGE_MANAGER=apt
TERMUX_APP_PID=8327
TERMUX_APP__DATA_DIR=/data/user/0/com.termux
TERMUX_APP__LEGACY_DATA_DIR=/data/data/com.termux
TERMUX_APP__SE_FILE_CONTEXT=u:object_r:app_data_file:s0:c5,c259,c512,c768
TERMUX_APP__SE_INFO=default:targetSdkVersion=28:complete
TERMUX_IS_DEBUGGABLE_BUILD=0
TERMUX_MAIN_PACKAGE_FORMAT=debian
TERMUX_VERSION=0.118.3
TERMUX__HOME=/data/data/com.termux/files/home
TERMUX__PREFIX=/data/data/com.termux/files/usr
TERMUX__ROOTFS_DIR=/data/data/com.termux/files
TERMUX__SE_PROCESS_CONTEXT=u:r:untrusted_app_27:s0:c5,c259,c512,c768
TERMUX__USER_ID=0
Packages CPU architecture:
aarch64
Subscribed repositories:
# sources.list
deb https://packages-cf.termux.dev/apt/termux-main stable main
Updatable packages:
openjdk-17-x/stable 17.0.16-2 aarch64 [upgradable from: 17.0.16-1]
openjdk-17/stable 17.0.16-2 aarch64 [upgradable from: 17.0.16-1]
openjdk-21-x/stable 21.0.8-1 aarch64 [upgradable from: 21.0.8]
openjdk-21/stable 21.0.8-1 aarch64 [upgradable from: 21.0.8]
termux-tools version:
1.45.0
Android version:
15
Kernel build information:
Linux localhost 5.4.242-30958140-abG996NKSS9HYE5 #1 SMP PREEMPT Wed May 21 09:56:38 KST 2025 aarch64 Android
Device manufacturer:
samsung
Device model:
SM-G996N
Supported ABIs:
SUPPORTED_ABIS: arm64-v8a,armeabi-v7a,armeabi
SUPPORTED_32_BIT_ABIS: armeabi-v7a,armeabi
SUPPORTED_64_BIT_ABIS: arm64-v8a
LD Variables:
LD_LIBRARY_PATH=
LD_PRELOAD=/data/data/com.termux/files/usr/lib/libtermux-exec-ld-preload.so
Installed termux plugins:
com.termux.widget versionCode:1000
com.termux.api versionCode:1001
