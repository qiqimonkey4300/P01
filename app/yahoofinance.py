# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

"""
Yahoo Finance

Handles all API queries and YFinance-related functionality.
"""

import base64
import datetime
import io
import json

import requests
import matplotlib

# Supress GUI output
matplotlib.use("Agg")

import matplotlib.pyplot as plt

with open("keys/key_yahoofinance.txt", "r", encoding="utf-8") as key:
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


def get_formatted_value(source: dict, key: str) -> str:
    """Returns the formatted value of the given dictionary entry or the empty
    string if it doesn't exist."""

    if key not in source or "fmt" not in source[key]:
        return "N/A"
    return source[key]["fmt"]


def summary_data(ticker: str) -> dict:
    """Returns information about the stock associated with the given ticker
    symbol using the Yahoo Finance API."""
    params = {"lang": "en", "modules": "summaryDetail,price"}
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

        if data["quoteSummary"]["result"] is None:
            return None

        results = data["quoteSummary"]["result"][0]
        price_data = results["price"]
        summary_detail = results["summaryDetail"]

        currency = price_data["currencySymbol"]

        key_stats = {
            "current_price": currency
            + get_formatted_value(price_data, "regularMarketPrice"),
            "market_cap": currency + get_formatted_value(price_data, "marketCap"),
            "dividend_rate": get_formatted_value(summary_detail, "dividendRate"),
            "dividend_yield": get_formatted_value(summary_detail, "dividendYield"),
            "payout_ratio": get_formatted_value(summary_detail, "payoutRatio"),
            "beta": get_formatted_value(summary_detail, "payoutRatio"),
            "trailing_pe": get_formatted_value(summary_detail, "trailingPE"),
        }

        return key_stats

    except json.decoder.JSONDecodeError:
        return None


def price_chart(ticker: str) -> str:
    """Returns a chart depicting the stock price over the past five days in a
    base64 string."""
    params = {"lang": "en", "range": "6mo", "interval": "1d"}
    headers = {"x-api-key": YFA_KEY}
    api_request = requests.request(
        "GET",
        f"https://yfapi.net/v8/finance/chart/{ticker}",
        headers=headers,
        params=params,
    )

    if api_request.status_code != requests.codes.ok:  # pylint: disable=no-member
        return None

    try:
        chart_data = api_request.json()
        if "chart" not in chart_data:
            return None

        timestamps = chart_data["chart"]["result"][0]["timestamp"]
        times = [datetime.datetime.fromtimestamp(timestamp) for timestamp in timestamps]
        prices = chart_data["chart"]["result"][0]["indicators"]["quote"][0]["low"]
        currency = chart_data["chart"]["result"][0]["meta"]["currency"]

        s = io.BytesIO()
        plt.plot(times, prices)
        plt.ylabel(f"Price ({currency})")
        plt.xlabel("Date")
        plt.title(f"Six-Month Prices for {ticker}")
        plt.savefig(s, format="png", bbox_inches="tight")
        plt.close()

        output_string = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")

        return output_string

    except json.decoder.JSONDecodeError:
        return None


def full_name(ticker: str) -> str:
    """Returns the full name of a company given its stock ticker."""
    params = {"lang": "en", "symbols": ticker}
    headers = {"x-api-key": YFA_KEY}
    api_request = requests.request(
        "GET",
        "https://yfapi.net/v6/finance/quote",
        headers=headers,
        params=params,
    )

    if api_request.status_code != requests.codes.ok:  # pylint: disable=no-member
        return None

    try:
        data = api_request.json()
        if "quoteResponse" not in data:
            return None

        results = data["quoteResponse"]["result"][0]
        if "longName" in results:
            return results["longName"]
        else:
            return None

    except json.decoder.JSONDecodeError:
        return None


if __name__ == "__main__":
    summary_data("GE")
