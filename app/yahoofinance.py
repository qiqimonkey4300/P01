# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

"""
Yahoo Finance

Handles all API queries and YFinance-related functionality.
"""


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

    if api_request.status_code != requests.codes.ok:  # pylint: disable=no-member
        return None

    try:
        results = api_request.json()
        if "ResultSet" not in results:
            return None

        return results["ResultSet"]["Result"]

    except json.decoder.JSONDecodeError:
        return None
