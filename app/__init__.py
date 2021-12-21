# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

from os import urandom

from flask import Flask, render_template, redirect, session, url_for, request

from user import create_user, authenticate_user, get_user_id, get_favorites
from styvio import Stock
from yahoofinance import YF

app = Flask(__name__)
app.secret_key = urandom(32)


@app.route("/", methods=["GET", "POST"])
def index():

    # finds possible tickers from what's searched
    if request.method == "POST":
        search_query = request.form.get("searchquery")
        # print(search_query)
        s = YF(search_query)
        search_results = s.autocomplete()
        return render_template("search.html", search_results = search_results)

    if "username" in session:
        username = session["username"]
        favorites = get_favorites(get_user_id(username))

        return render_template("home.html", username=username, favorites=favorites)
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
    return redirect(url_for("login"))  # should be login


@app.route("/login", methods=["GET", "POST"])
def login():
    """Displays login form and handles form response."""
    if "username" in session:
        return redirect(url_for("index"))

    # GET request: display the form
    if request.method == "GET":
        return render_template("login.html")

    # POST request: handle the form response and redirect
    username = request.form.get("username", default="")
    password = request.form.get("password", default="")

    if authenticate_user(username, password):
        session["username"] = username
        return redirect(url_for("index"))

    return render_template("login.html", error="incorrect")


@app.route("/logout")
def logout():
    """Logs out the current user."""

    if "username" in session:
        del session["username"]
    return redirect(url_for("index"))


@app.route("/stock/<ticker>")
def stock(ticker):
    stock_obj = Stock(ticker)
    return stock_obj.get_short_name()


if __name__ == "__main__":
    app.debug = True
    app.run()
