import json
import math
from dataclasses import dataclass
from typing import Union

import numpy as np
import pandas as pd
import pkg_resources
import requests

# API from 国土交通省
# web: https://www.land.mlit.go.jp/webland/api.html

CITYSEARCH_EN_URL = "https://www.land.mlit.go.jp/webland_english/api/CitySearch"
TRADESEARCH_EN_URL = "https://www.land.mlit.go.jp/webland_english/api/TradeListSearch"
EN_PREF_CODE_JSON_PATH = pkg_resources.resource_filename(
    "j_realty_api.j_realty_en", "data/pref-code-en.json"
)


@dataclass
class CityCode:

    """
    都道府県名を渡すと、その都道府県の市区町村名とコードの格納された
    データが返される。
    市区町村名を指定すると、市区町村コードが返される
    すべて大文字で入ってきた場合などの対応を考える必要あり。
    """

    pref_name: str
    base_path: str = CITYSEARCH_EN_URL

    @property
    def pref_code(self) -> str:
        """
        都道府県名からコードを探す
        """
        with open(EN_PREF_CODE_JSON_PATH, "r", encoding="utf-8") as f:
            pref_code_json = json.load(f)
        for p_name, p_code in pref_code_json.items():
            if p_name.startswith(self.pref_name.lower()):
                return p_code
        raise Exception(f"No pref_code found for {self.pref_name}")

    @property
    def city_json(self):
        r = requests.get(self.base_path, params={"area": self.pref_code})
        city_json = r.json()
        new_list = list()
        for d in city_json['data']:
            d['name'] = d['name'].lower()
            new_list.append(d)
        city_json['data'] = new_list
        return city_json

    def city_code(self, city_name: str):
        for d in self.city_json.get("data", []):
            if d["name"].startswith(city_name.lower()):
                return d["id"]
        raise Exception(f"No city_code found for {city_name}.")


@dataclass
class PropTransactions:
    
    pref_code: str
    city_code: str
    from_dt: int = 20221
    to_dt: int = 20223
    base_url: str = TRADESEARCH_EN_URL

    def get_data(self):
        params = {
            "from": self.from_dt,
            "to": self.to_dt,
            "area": self.pref_code,
            "city": self.city_code,
        }
        r = requests.get(self.base_url, params=params)
        if r.status_code == 200:
            df = pd.DataFrame(r.json()["data"])
            return df
        else:
            raise Exception(f"Status_code: {r.status_code}")


if __name__ == "__main__":
    k = CityCode("Kyoto")
    pref_code = k.pref_code
    city_code = k.city_code('Kyoto')
    print(pref_code)
    print(city_code)