from j_realty_api import j_realty_en as je

cc = je.CityCode('kyoto')
pref_code = cc.pref_code
city_code = cc.city_code('kyoto')
pt = je.PropTransactions(
    pref_code,
    city_code,
)

df = pt.get_data()
df.to_csv('./tests/data/test.csv')
print(df.info())
