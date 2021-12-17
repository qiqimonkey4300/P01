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


class Stock:
    """Handles information for a given stock regarding Styvio data."""

    def __init__(self, ticker: str):
        self.ticker = ticker

    def get_stock_sentiment(self) -> dict:
        """Uses the Styvio API to retrieve stock sentiment information."""

        # api_request = requests.get(f"https://www.styvio.com/apiV2/sentiment/{self.ticker}/{STYVIO_KEY}")
        # return api_request.json()

        return {
            "connectedUser": "Clue88",
            "apiSubscription": "Trial Tier (25 queries)",
            "totalQueries": 4,
            "ticker": "AAPL",
            "companyInformation": {
                "name": "Apple Inc.",
                "logoURL": "https://logo.clearbit.com/apple.com",
            },
            "rWallSstreetBetsSentiment": {
                "percentBullish": 23.531806737663853,
                "percentBearish": 17.744721348109167,
                "percentNeutral": 58.72347191422699,
                "occurences": 1,
            },
            "rStocksSentiement": {
                "percentBullish": 30.27002963760565,
                "percentBearish": 19.301051107325765,
                "percentNeutral": 50.428919255068585,
                "occurences": 6,
            },
            "rStockMarketSentiment": {
                "percentBullish": 32.50510707786066,
                "percentBearish": 22.21821236596297,
                "percentNeutral": 45.276680556176366,
                "occurences": 4,
            },
            "rInvestingSentiment": {
                "percentBullish": 0.0,
                "percentBearish": 0.0,
                "percentNeutral": 0.0,
                "occurences": 0,
            },
            "stockTwitsSentiment": {
                "percentBullish": 31.968339244128618,
                "percentBearish": 16.333464390649098,
                "percentNeutral": 51.69819636522228,
                "occurences": "All posts scanned",
            },
            "overallSentiment": {
                "totalBullishSentiment": 29.568820674314694,
                "totalBearishSentiment": 18.89936230301175,
                "overallSocialRating": "Bullish",
            },
        }


if __name__ == "__main__":
    apple = Stock("AAPL")
    print(apple.get_short_name())
