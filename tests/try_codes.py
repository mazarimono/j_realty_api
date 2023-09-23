from j_realty_api import j_realty_jp as jrp

pref_code = '00'
city_code = '0000'

pt = jrp.PropTransactions(pref_code, city_code)
pt.get_data()