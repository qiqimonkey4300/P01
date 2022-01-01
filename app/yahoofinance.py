# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04


import json

import requests

with open("api_keys/yahoofinance.txt", "r", encoding="utf-8") as key:
    YFA_KEY = key.read().strip()


def autocomplete(query: str) -> dict:
    """Returns possible search query autocomplete results."""
    params = {"lang": "en", "query": query}
    headers = {"x-api-key": YFA_KEY}
    api_request = requests.request(
        "GET",
        "https://yfapi.net/v6/finance/autocomplete/",
        headers=headers,
        params=params,
    )

    if api_request.status_code != requests.codes.ok:
        return None

    try:
        results = api_request.json()
        if "ResultSet" not in results:
            return None

        return results["ResultSet"]["Result"]

    except json.decoder.JSONDecodeError:
        return None


# class YF:
#     def __init__(self, searchquery: str):
#         self.searchquery = searchquery

#     def autocomplete(self) -> dict:
#         url = "https://yfapi.net/v6/finance/autocomplete/"
#         querystring = {"lang": "en", "query": self.searchquery}
#         headers = {"x-api-key": YFA_KEY}
#         response = requests.request("GET", url, headers=headers, params=querystring)
#         data = json.loads(response.content)
#         return data

#     def summary(self) -> dict:
#         url = "https://yfapi.net/v11/finance/quoteSummary/"
#         querystring = {
#             "lang": "en",
#             "region": "US",
#             "modules": "summaryDetail,assetProfile,defaultKeyStatistics",
#             "symbol": self.searchquery,
#         }
#         url += querystring["symbol"]
#         headers = {"x-api-key": YFA_KEY}
#         response = requests.request("GET", url, headers=headers, params=querystring)
#         data = json.loads(response.content)
#         return data

#     # def recs(self) -> dict:
#     #     ..


# if __name__ == "__main__":
#     apple = YF("AAPL")
#     print(apple.summary())
