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


def summary_data(ticker: str) -> dict:
    """Returns information about the stock associated with the given ticker
    symbol using the Yahoo Finance API."""
    params = {"lang": "en", "modules": "financialData,summaryDetail"}
    headers = {"x-api-key": YFA_KEY}
    api_request = requests.request(
        "GET",
        f"https://yfapi.net/v11/finance/quoteSummary/{ticker}",
        headers=headers,
        params=params,
    )

    if api_request.status_code != requests.codes.ok:  # pylint: disable=no-member
        return None

    try:
        data = api_request.json()
        if "quoteSummary" not in data:
            return None

        results = data["quoteSummary"]["result"][0]
        financial_data = results["financialData"]
        summary_detail = results["summaryDetail"]

        currency = financial_data["financialCurrency"]

        key_stats = {
            "current_price": currency + " " + financial_data["currentPrice"]["fmt"],
            "market_cap": currency + " " + summary_detail["marketCap"]["fmt"],
            "dividend_rate": summary_detail["dividendRate"]["fmt"],
            "dividend_yield": summary_detail["dividendYield"]["fmt"],
            "payout_ratio": summary_detail["payoutRatio"]["fmt"],
            "beta": summary_detail["payoutRatio"]["fmt"],
            "trailing_pe": summary_detail["trailingPE"]["fmt"],
        }

        return key_stats

    except json.decoder.JSONDecodeError:
        return None
