import sqlite3

def get_connection():
    """Возвращает соединение с базой данных"""
    return sqlite3.connect('/storage/emulated/0/FOOTBALL/db/football.db')
