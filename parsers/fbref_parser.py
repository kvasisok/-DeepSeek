import requests
from selectolax.parser import HTMLParser

def parse_xg(html):
    tree = HTMLParser(html)
    xg_node = tree.css_first('td[data-stat="xg"]')
    shots_node = tree.css_first('td[data-stat="shots"]')
    return {
        'xg': float(xg_node.text()) if xg_node else 0.0,
        'shots': int(shots_node.text()) if shots_node else 0
    }

def parse_fbref(url):
    try:
        resp = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=10)
        return parse_xg(resp.text) if resp.status_code == 200 else None
    except:
        return None
