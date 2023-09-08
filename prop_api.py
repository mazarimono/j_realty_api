from dataclasses import dataclass
import json
import pandas as pd
import requests


@dataclass
class CityCode:

    '''
    都道府県名を渡すと、その都道府県の市区町村名とコードの格納された
    データが返される。
    市区町村名を指定すると、市区町村コードが返される
    '''

    pref_name: str
    base_path: str = 'https://www.land.mlit.go.jp/webland/api/CitySearch'

    @property
    def pref_code(self) -> str:
        '''
        都道府県名からコードを探す
        '''
        with open('./data/japan-pref-code.json', 'r', encoding='utf-8') as f:
            pref_code = json.load(f)
        for p_name, p_code in pref_code.items():
            if p_name.startswith(self.pref_name):
                return p_code
            else:
                pass
        raise Exception('There was no pref_code corresponding to the pref_name.')
    

    @property
    def city_json(self):
        r = requests.get(self.base_path, params={'area': self.pref_code})
        return r.json()
    

    def city_code(self, city_name: str):
        for d in self.city_json['data']:
            if d['name'].startswith(city_name):
                return d['id']
        else:
            pass
        raise Exception('There was no city_code corresponding to the city_name.')


@dataclass
class PropTransactions:

    area: str
    city: str
    from_dt: int = 20221
    to_dt: int = 20223
    base_url: str = 'https://www.land.mlit.go.jp/webland/api/TradeListSearch'

    '''
    area: str
        都道府県コード
    city: str
        市区町村コード
    from_dt: str
    to_dt: str
        'YYYYQ' の形で表現される。Q は四半期
        形式はYYYYN（数字5桁）
        YYYY … 西暦
        N … 1～4（1:1月～3月、2:4月～6月、3:7月～10月、4:11月～12月）
        ※20053（平成17年第３四半期）より指定可能    
    '''

    def get_data(self):
        params = {
            'from': self.from_dt,
            'to': self.to_dt,
            'area': self.area,
            'city': self.city
        }
        r = requests.get(self.base_url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json()['data'])
            return df
        else:
            raise Exception('ちょっとおかしいようです')



if __name__ == '__main__':
    t = CityCode('京都')
    pref_code = t.pref_code
    city_code = t.city_code('京都市')
    kt = PropTransactions(
        pref_code,
        city_code,
        20223,
        20231
    )
    df = kt.get_data()
    print(df.head())
