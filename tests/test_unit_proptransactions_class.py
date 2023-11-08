from unittest.mock import Mock, patch

import pandas as pd
import pytest

from j_realty_api import j_realty_en, j_realty_jp


class TestEnPropTransactions:

    pref_code = '26'
    city_code = '26100'

    def test_get_data_success(self): 
        pt = j_realty_en.PropTransactions(self.pref_code, self.city_code)
        df = pt.get_data()
        assert isinstance(df, pd.DataFrame)


    def test_data_to_forex(self):
        pt = j_realty_en.PropTransactions(self.pref_code, self.city_code)
        df = pt.get_data()
        df = pt.to_forex(df, 'USD')
        assert isinstance(df, pd.DataFrame)
        

    # def test_get_data_fail(self):
    #     pref_code = '99'
    #     city_code = '99999'
    #     pt = j_realty_en.PropTransactions(pref_code, city_code)
    #     with pytest.raises(KeyError):
    #         pt.get_data()
