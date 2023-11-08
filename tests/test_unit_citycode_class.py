import pytest

from j_realty_api import j_realty_en as jrn
from j_realty_api import j_realty_jp as jrp


class TestJrnCityCode:
    def test_prefcode(self):
        kyoto_code = jrn.CityCode("Kyoto").pref_code
        osaka_code = jrn.CityCode("Osaka").pref_code
        hokkaido_code = jrn.CityCode("Hokkai").pref_code
        tokyo_code = jrn.CityCode("TOKY").pref_code
        assert kyoto_code == "26"
        assert osaka_code == "27"
        assert hokkaido_code == "01"
        assert tokyo_code == "13"

    def test_error_in_prefcode(self):
        with pytest.raises(Exception):
            jrn.CityCode("KITAOJI").pref_code()

    def test_city_code_json(self):
        kyoto_json = jrn.CityCode("Kyoto").city_json
        assert isinstance(kyoto_json, dict)
        assert "data" in kyoto_json
        assert "status" in kyoto_json
        assert isinstance(kyoto_json["data"], list)

    def test_citycode(self):
        k = jrn.CityCode("Kyoto")
        k_city = k.city_code("Kyoto")
        kami_city = k.city_code("Kamigyo")
        yama_city = k.city_code("Yamashina")
        assert k_city == "26100"
        assert kami_city == "26102"
        assert yama_city == "26110"


class TestJrpCityCode:
    def test_prefcode(self):
        kyoto_code = jrp.CityCode("京都").pref_code
        osaka_code = jrp.CityCode("大阪").pref_code
        hokkaido_code = jrp.CityCode("北海").pref_code
        tokyo_code = jrp.CityCode("東京").pref_code
        assert kyoto_code == "26"
        assert osaka_code == "27"
        assert hokkaido_code == "01"
        assert tokyo_code == "13"

    def test_error_in_prefcode(self):
        with pytest.raises(Exception):
            jrp.CityCode("五条").pref_code()

    def test_city_code_json(self):
        kyoto_json = jrp.CityCode("京都").city_json
        assert isinstance(kyoto_json, dict)
        assert "data" in kyoto_json
        assert "status" in kyoto_json
        assert isinstance(kyoto_json["data"], list)

    def test_citycode(self):
        k = jrp.CityCode("京都")
        k_city = k.city_code("京都")
        kami_city = k.city_code("上京")
        yama_city = k.city_code("山科")
        assert k_city == "26100"
        assert kami_city == "26102"
        assert yama_city == "26110"
