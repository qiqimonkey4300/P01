# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

import requests
import json

from flask import Flask, render_template, redirect, session, url_for, request

from auth import create_user
from styvio import Stock

app = Flask(__name__)
#
# with open("api_keys/yahoofinance.txt", "r", encoding="utf-8") as key:
#     YFA_KEY = key.read().strip()
#
# url = "https://yfapi.net/v6/finance/recommendationsbysymbol/AAPL"
#
# querystring = {"symbols":"AAPL"}
#
# headers = {'x-api-key': YFA_KEY}
#
# response = requests.request("GET", url, headers=headers, params=querystring)
# data = json.loads(response.content)

# print(response.text)

@app.route("/")
def index():
    return render_template("guest.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Displays registration form and handles form response."""
    if "username" in session:
        return redirect(url_for("index"))

    # GET request: display the form
    if request.method == "GET":
        return render_template("register.html")

    # POST request: handle the form response and redirect
    username = request.form.get("username", default="")
    password = request.form.get("password", default="")
    password_check = request.form.get("password_check", default="")

    errors = create_user(username, password, password_check)
    if errors:
        return render_template("register.html", errors=errors)

    # Maybe put a flash message here to confirm everything works
    return redirect(url_for("index"))  # should be login


@app.route("/stock/<ticker>")
def stock(ticker):
    stock_obj = Stock(ticker)
    return stock_obj.get_short_name()


if __name__ == "__main__":
    app.debug = True
    app.run()
