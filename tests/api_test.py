import requests

TRADESEARCH_EN_URL = "https://www.land.mlit.go.jp/webland_english/api/TradeListSearch"

pref_code: str = '26'
city_code: str = '26100'
from_dt: int = 20222
to_dt: int = 20223
base_url: str = TRADESEARCH_EN_URL


params = {
    'from': from_dt,
    'to': to_dt,
    'area': pref_code,
    'city': city_code
}
r = requests.get(base_url, params)
if r.status_code:
    print(r.json())