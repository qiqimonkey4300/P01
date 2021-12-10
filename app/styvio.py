# no-stall-GICS -- Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 -- no-stock-GICS

"""
Styvio

Handles all API queries and Styvio-related functionality.
"""

import requests


with open("api_keys/styvio.txt", "r", encoding="utf-8") as key:
    STYVIO_KEY = key.read().strip()


def get_stock_info(ticker: str) -> dict:
    """Uses the Styvio API to retrieve stock information for the given ticker
    symbol."""

    api_request = requests.get(f"https://www.styvio.com/apiV2/{ticker}/{STYVIO_KEY}")
    return api_request.json()


if __name__ == "__main__":
    print(get_stock_info("AAPL"))
