# no-stall-GICS -- Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 -- no-stock-GICS
# 2022-01-04

"""
Styvio

Handles all API queries and Styvio-related functionality.
"""

import json

import requests


with open("api_keys/key_styvio.txt", "r", encoding="utf-8") as key:
    STYVIO_KEY = key.read().strip()


def get_stock_sentiment(ticker: str) -> str:
    """Uses the Styvio API to retrieve stock sentiment information and
    returns whether the user should buy or sell shares of that stock."""

    api_request = requests.get(
        f"https://www.styvio.com/apiV2/sentiment/{ticker}/{STYVIO_KEY}"
    )

    if api_request.status_code != requests.codes.ok:  # pylint: disable=no-member
        return None

    try:
        sentiment = api_request.json()
        if "overallSentiment" not in sentiment:
            return None

        return {
            "rating": sentiment["overallSentiment"]["overallSocialRating"],
            "name": sentiment["companyInformation"]["name"],
            "logo": sentiment["companyInformation"]["logoURL"],
        }

    except json.decoder.JSONDecodeError:
        return None
