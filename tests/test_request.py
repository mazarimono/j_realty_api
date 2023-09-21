import requests
import pandas as pd

TRADESEARCH_EN_URL = "https://www.land.mlit.go.jp/webland_english/api/TradeListSearch"

def test_requests(pref_code, city_code):
    params = {
        'from': 20221,
        'to': 20223,
        'area': pref_code,
        'city': city_code
    }
    r = requests.get(
        TRADESEARCH_EN_URL,
        params=params
    )
    df = pd.DataFrame(r.json()['data'])
    return df

if __name__ == '__main__':
    df = test_requests(26, 26100)
    print(df.head(10))
    df.to_csv('tests/data/transactions_en.csv')
