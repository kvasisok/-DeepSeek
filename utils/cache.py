import json
import os
from datetime import datetime

CACHE_DIR = os.path.expanduser('~/.football_cache')

def get_cache(key):
    try:
        with open(f"{CACHE_DIR}/{key}.json", 'r') as f:
            return json.load(f)
    except:
        return None

def set_cache(key, data, ttl=3600):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(f"{CACHE_DIR}/{key}.json", 'w') as f:
        json.dump({
            'expires': datetime.now().timestamp() + ttl,
            'data': data
        }, f)
