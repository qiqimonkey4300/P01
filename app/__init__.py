# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

import requests

from flask import Flask, render_template

from styvio import Stock

app = Flask(__name__)

# url = "https://yfapi.net/v6/finance/recommendationsbysymbol"
#
# querystring = {"symbols":"AAPL,BTC-USD,EURUSD=X"}
#
# headers = {
#     'x-api-key': ""
#     }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
#
# print(response.text)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/stock/<ticker>")
def stock(ticker):
     stock_obj = Stock(ticker)
     return stock_obj.get_short_name()


if __name__ == "__main__":
    app.debug = True
    app.run()
