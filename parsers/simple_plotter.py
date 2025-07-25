import os
from datetime import datetime, timedelta
import shutil

def setup_dirs():
    """Создает необходимые директории"""
    # Основное хранилище в Termux
    termux_dir = os.path.expanduser('~/FOOTBALL_APP/reports')
    os.makedirs(termux_dir, exist_ok=True)
    
    # Папка в Download для быстрого доступа
    download_dir = '/sdcard/Download/FootballReports'
    os.makedirs(download_dir, exist_ok=True)
    
    return termux_dir, download_dir

def clean_old_files(dir_path, days_to_keep=7):
    """Удаляет файлы старше days_to_keep дней"""
    cutoff = datetime.now() - timedelta(days=days_to_keep)
    
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if os.path.isfile(filepath):
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if mtime < cutoff:
                os.remove(filepath)
                print(f"Удален старый файл: {filename}")

def create_report(report_data):
    """Создает и сохраняет отчет"""
    try:
        termux_dir, download_dir = setup_dirs()
        
        # Генерация имени файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{timestamp}.html"
        
        # HTML-содержимое
        html_content = f"""<!DOCTYPE html><html><head>
            <meta charset="UTF-8">
            <title>Отчет {timestamp}</title>
            <style>
                body {{ font-family: Arial; padding: 20px; }}
                .stat-card {{ background: #f5f5f5; padding: 15px; margin-bottom: 10px; }}
            </style>
        </head><body>
            <h2>Футбольная статистика</h2>
            <div class="stat-card">
                <h3>Атака</h3>
                <p>Удары: {report_data['shots_on_target']}/{report_data['shots']}</p>
                <p>Точность: {report_data['shots_on_target']/report_data['shots']:.0%}</p>
            </div>
            <div class="stat-card">
                <h3>Защита</h3>
                <p>Сейвы: {report_data['gk_save_percent']}%</p>
            </div>
            <p>Сгенерировано: {datetime.now().strftime("%d.%m.%Y %H:%M")}</p>
        </body></html>"""
        
        # Сохранение в Termux (долгосрочное хранение)
        termux_path = os.path.join(termux_dir, filename)
        with open(termux_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Копия в Download (временное хранение)
        download_path = os.path.join(download_dir, filename)
        shutil.copy2(termux_path, download_path)
        
        # Очистка старых файлов только в Termux
        clean_old_files(termux_dir)
        
        print(f"\n✅ Отчет создан:\nОсновной: {termux_path}\nКопия: {download_path}")
        
    except Exception as e:
        print(f"⚠️ Ошибка: {str(e)}")
