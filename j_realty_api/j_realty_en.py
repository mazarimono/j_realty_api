import json
import math
from dataclasses import dataclass
from datetime import datetime
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
    A class that, when given a prefecture name, returns data containing
    the names and codes of the municipalities in that prefecture. When a
    municipality name is specified, it returns the municipality code.

    """

    pref_name: str
    base_path: str = CITYSEARCH_EN_URL

    @property
    def pref_code(self) -> str:
        """
        search pref_code from JSON with pref_name
        Returns:
            str: pref_code
        """
        with open(EN_PREF_CODE_JSON_PATH, "r", encoding="utf-8") as f:
            pref_code_json = json.load(f)
        for p_name, p_code in pref_code_json.items():
            if p_name.startswith(self.pref_name.lower()):
                return p_code
        raise Exception(f"No pref_code found for {self.pref_name}")

    @property
    def city_json(self) -> dict[str]:
        """
        api returns each pref's city_codes json.
        Returns:
            Dict[str]: JSON with {'cityname' : 'citycode'}
        """
        r = requests.get(self.base_path, params={"area": self.pref_code})
        city_json = r.json()
        new_list = list()
        for d in city_json["data"]:
            d["name"] = d["name"].lower()
            new_list.append(d)
        city_json["data"] = new_list
        return city_json

    def city_code(self, city_name: str) -> str:
        """
        Searches for the city code corresponding to the provided
        city name from the city_json.

        Args:
            city_name str: City name for which to find the city code.
        Returns:
            str: city code

        """
        for d in self.city_json.get("data", []):
            if d["name"].startswith(city_name.lower()):
                return d["id"]
        raise Exception(f"No city_code found for {city_name}.")


@dataclass
class PropTransactions:

    """
    A class that retrieves property transaction data based on the specified parameters
    such as prefecture code, city code, and date range from a given API endpoint.
    """

    pref_code: str
    city_code: str
    from_dt: int = 20222
    to_dt: int = 20223
    base_url: str = TRADESEARCH_EN_URL

    def get_data(self) -> pd.DataFrame:
        """
        Sends a GET request to the API with the specified parameters and retrieves
        property transaction data.

        The method constructs a DataFrame from the received JSON data and returns it.

        Returns:
            pd.DataFrame: A DataFrame containing the property transaction data.

        """
        params = {
            "from": self.from_dt,
            "to": self.to_dt,
            "area": self.pref_code,
            "city": self.city_code,
        }
        r = requests.get(self.base_url, params=params)
        if r.status_code == 200:
            try:
                df = pd.DataFrame(r.json()["data"])
                df["Period"] = df["Period"].map(self.custom_to_datetime)
                # for col in ['TradePrice']: # 'Area'は文字列のものが入っているので、対応を考えて追加する
                #     df[col] = df[col].astype(int)
                return df
            except KeyError:
                print(
                    f"""KeyError: The received JSON does not contain the expected "data" key.
                      pref_code: {self.pref_code}, city_code: {self.city_code}, 
                      from_dt: {self.from_dt}, to_dt: {self.to_dt}
                      """
                )
        else:
            raise Exception(f"Status_code: {r.status_code}")

    def custom_to_datetime(self, p_str):
        split_str = p_str.split(" ")
        year = int(split_str[2])
        q = split_str[0]
        if q == "1st":
            qt = self.dt_to_qt(year, 2)
            return qt
        elif q == "2nd":
            qt = self.dt_to_qt(year, 5)
            return qt
        elif q == "3rd":
            qt = self.dt_to_qt(year, 8)
            return qt
        elif q == "4th":
            qt = self.dt_to_qt(year, 11)
            return qt
        else:
            raise ValueError(f"invalid quater: {p_str}")

    def dt_to_qt(self, year, month):
        dt = datetime(year, month, 1)
        ts = pd.Timestamp(dt)
        qt = ts.to_period("Q")
        return qt


if __name__ == "__main__":
    k = CityCode("Kyoto")
    pref_code = k.pref_code
    city_code = k.city_code("Kyoto")
    print(pref_code)
    print(city_code)
