# Football Predictor Roadmap

## Цели
- Прогнозирование: исходы, угловые, карточки, тоталы
- Сбор всей статистики (история + live)
- Учёт составов, травм и внешних факторов

## Этапы

### Этап 1: Базовый парсинг (1 нед)
- [x] API football-data.org (текущие матчи)
- [ ] Исторические данные (доп. источники)
- [ ] Transfermarkt (составы/травмы)

### Этап 2: Расширенная статистика (2 нед)
- [ ] BetExplorer (коэффициенты)
- [ ] SofaScore (xG, передачи)
- [ ] Погодные API

### Этап 3: Модели прогноза (3 нед)
- [ ] Базовые алгоритмы
- [ ] ML-модель для исходов
- [ ] Статистические модели (угловые/карточки)

### Этап 4: Автоматизация (4 нед)
- [ ] Ежедневное обновление
- [ ] Telegram-бот для алёртов
- [ ] Экспорт в CSV/БД

## Требуемые данные
```json
{
  "match_data": ["score", "shots", "possession", "corners", "cards"],
  "team_data": ["form", "lineups", "injuries"],
  "external": ["weather", "referee_stats"]
}

### 2. Автоматизация выполнения
Добавим в `.projectrc` проверку прогресса:
```bash
cat >> /storage/emulated/0/Documents/FOOTBALL_APP/.projectrc <<'EOF'

function check_progress() {
    echo "Текущий прогресс:"
    grep -E '\[(x| )\]' $FOOTBALL_PROJECT_DIR/roadmap.md
}
