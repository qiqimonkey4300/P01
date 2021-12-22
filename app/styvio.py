# no-stall-GICS -- Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 -- no-stock-GICS

"""
Styvio

Handles all API queries and Styvio-related functionality.
"""

import json

import requests


with open("api_keys/styvio.txt", "r", encoding="utf-8") as key:
    STYVIO_KEY = key.read().strip()


class Stock:
    """Handles information for a given stock regarding Styvio data."""

    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_stock_sentiment(self) -> str:
        """Uses the Styvio API to retrieve stock sentiment information and
        returns whether the user should buy or sell shares of that stock."""

        api_request = requests.get(
            f"https://www.styvio.com/apiV2/sentiment/{self.ticker}/{STYVIO_KEY}"
        )

        if api_request.status_code != requests.codes.ok:
            return None

        try:
            sentiment = api_request.json()
            if "overallSentiment" not in sentiment:
                return None

            rating = sentiment["overallSentiment"]["overallSocialRating"]
            return "SELL" if rating == "Bearish" else "BUY"

        except json.decoder.JSONDecodeError:
            return None


if __name__ == "__main__":
    apple = Stock("AAPL")
    print(apple.get_stock_sentiment())
