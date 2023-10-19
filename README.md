# j_realty_api: Knowing the real estate transaction prices in Japan.

## What is it?

The j_realty_api is a wrapper for an API that allows you to retrieve real estate transaction prices in Japan, utilizing the [Real Estate Transaction Price Information Retrieval API](https://www.land.mlit.go.jp/webland/api.html) provided by Japan's Ministry of Land, Infrastructure, Transport and Tourism. It makes the use of the API more convenient. It supports both Japanese and English APIs.

A feature of the tool is that it includes a tool to obtain prefecture codes and municipality codes, making it easier to search for data.

j_realty_apiは、日本の国土交通省が出している[不動産取引価格情報取得API](https://www.land.mlit.go.jp/webland/api.html)を使い、日本の不動産取引価格を取得できる、APIのラッパーです。APIの利用が容易になります。日本語API、英語APIの両方に対応しています。

ツールの特徴は、都道府県コードと市町村コードを取得できるツールを加えて、データを探しやすくした点です。

## Where to get it
The source code is currently hosted on Github at: [https://github.com/mazarimono/j_realty_api](https://github.com/mazarimono/j_realty_api)

## Installation

- インストール方法

```sh
pip install git+https://github.com/mazarimono/j_realty_api.git
```

## How to Use
### 使い方

- English
    - [sample notebook](https://github.com/mazarimono/j_realty_api/tree/main/samples/sample_j_realty_en.ipynb)

```python
# English
from j_realty_api import j_realty_en as jrn

j = j_realty_en.CityCode('Kyoto')
pref_code = j.pref_code
city_code = j.city_code('kyoto')
pt = jrn.PropTransactions(pref_code, city_code, 20223, 20224)
df = pt.get_data()

```

- 日本語
- [sample notebook](https://github.com/mazarimono/j_realty_api/tree/main/samples/sample_j_realty_jp.ipynb)

```python
from j_realty_api import j_realty_jp as jrp

j = jrp.CityCode('京都')
pref_code = j.pref_code
city_code = j.city_code('京都')
pt = jrp.PropTransactions(pref_code, city_code, 20223, 20224)
df = pt.get_data()
```


## Licence
MIT