# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

import requests
import json

from flask import Flask, render_template

from styvio import Stock

app = Flask(__name__)

# with open("api_keys/yahoofinance.txt", "r", encoding="utf-8") as key:
#     YFA_KEY = key.read().strip()
#
# url = "https://yfapi.net/v6/finance/quote"
#
# querystring = {"symbols":"AAPL,BTC-USD,EURUSD=X"}
#
# headers = {
    # 'x-api-key': YFA_KEY
#     }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
# data = json.loads(response.content)

@app.route("/")
def index():
    # return render_template('index.html', name = data["shortName"], currency = data["currency"], high = data["fiftyTwoWeekHigh"], low = data["fiftyTwoWeekLow"])
    return render_template("guest.html")


@app.route("/stock/<ticker>")
def stock(ticker):
     stock_obj = Stock(ticker)
     return stock_obj.get_short_name()


if __name__ == "__main__":
    app.debug = True
    app.run()
