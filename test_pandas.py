import pandas as pd
import numpy as np

# Тестовая DataFrame
data = {
    'Команда': ['Челси', 'ПСЖ', 'Барселона'],
    'xG': [1.8, 1.5, 2.1],
    'Удары': [15, 12, 18]
}

df = pd.DataFrame(data)
print("\nТест pandas:")
print(df)
print("\nСредний xG:", df['xG'].mean())
