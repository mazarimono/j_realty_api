from j_realty_api import j_realty_jp as jrp


if __name__ == "__main__":
    t = jrp.city_code('京都')
    print(t.city_code)
    print(t.city_json)