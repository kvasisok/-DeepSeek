import json
from pathlib import Path
from datetime import datetime
import os

PREDICTIONS_DIR = Path(__file__).parent.parent / 'db' / 'predictions'
PREDICTIONS_DIR.mkdir(parents=True, exist_ok=True)

def save_prediction(match_data, probabilities, report):
    """Сохранение прогноза с проверкой всех данных"""
    filename = f"pred_{datetime.now().strftime('%Y%m%d_%H%M')}_{match_data['id']}.json"
    filepath = PREDICTIONS_DIR / filename
    
    # Гарантируем наличие всех полей
    prediction_data = {
        'version': 1,  # Версия формата данных
        'match_info': {
            'id': str(match_data.get('id', '')),
            'home_team': match_data.get('home_team', ''),
            'away_team': match_data.get('away_team', ''),
            'date': match_data.get('date', ''),
            'time': match_data.get('time', ''),
            'competition': match_data.get('competition', '')
        },
        'probabilities': {
            'home': probabilities.get('home', 0),
            'draw': probabilities.get('draw', 0),
            'away': probabilities.get('away', 0)
        },
        'report': report,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    with open(filepath, 'w') as f:
        json.dump(prediction_data, f, indent=2)
    return filepath

def load_predictions():
    """Загрузка прогнозов с проверкой структуры"""
    predictions = []
    
    for file in PREDICTIONS_DIR.glob('*.json'):
        try:
            with open(file) as f:
                data = json.load(f)
                
            # Проверяем обязательные поля
            if not all(k in data for k in ['match_info', 'report']):
                continue
                
            # Добавляем недостающие поля для совместимости
            data.setdefault('created_at', datetime.now().isoformat())
            data['filename'] = file.name
            predictions.append(data)
            
        except (json.JSONDecodeError, KeyError):
            continue
    
    # Сортируем по дате создания (новые сначала)
    return sorted(predictions, key=lambda x: x.get('created_at', ''), reverse=True)

def delete_prediction(filename):
    """Удаление прогноза с проверкой"""
    try:
        filepath = PREDICTIONS_DIR / filename
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    except:
        return False

def get_prediction_by_match_id(match_id):
    """Поиск прогноза с обработкой ошибок"""
    for pred in load_predictions():
        try:
            if str(pred['match_info']['id']) == str(match_id):
                return pred
        except (KeyError, TypeError):
            continue
    return None
