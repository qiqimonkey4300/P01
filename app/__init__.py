# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# [2022-01-03]

from flask import Flask, render_template
app = Flask(__name__)

import requests

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
     return render_template('index.html' )

if __name__ == "__main__":
    app.debug = True
    app.run()
