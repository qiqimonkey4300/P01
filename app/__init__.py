# no-stall-GICS — Christopher Liu, Ivan Mijacika, Shyne Choi, Gavin McGinley
# SoftDev
# P01 — no-stock-GICS
# 2022-01-04

"""
App and Routes

Handles Flask routing for the app.
"""


from os import remove, urandom

from flask import Flask, render_template, redirect, session, url_for, request

from user import (
    create_user,
    authenticate_user,
    get_user_id,
    get_favorites,
    add_favorite,
    remove_favorite,
)
from styvio import get_stock_sentiment
from mediawiki import MW
from yahoofinance import autocomplete, summary_data, price_chart, full_name

app = Flask(__name__)
app.secret_key = urandom(32)


@app.route("/")
def index():
    """Displays homepage."""
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


@app.route("/search")
def search():
    """Displays a search result page containing possible autocomplete stock
    ticker symbols based on the search query."""

    if "searchquery" not in request.args or request.args.get("searchquery") == "":
        return redirect(url_for("index"))

    search_query = request.args.get("searchquery")
    autocomplete_results = autocomplete(search_query)

    favorites = None
    if "username" in session:
        favorites = get_favorites(get_user_id(session["username"]))

    return render_template(
        "search.html",
        search_query=search_query,
        autocomplete_results=autocomplete_results,
        favorites=favorites,
    )


@app.route("/stock/<ticker>")
def stock(ticker):
    """Displays detailed information about the stock associated with the given
    ticker symbol."""

    favorites = None
    is_favorite = False
    if "username" in session:
        favorites = get_favorites(get_user_id(session["username"]))
        if ticker in favorites:
            is_favorite = True

    key_stats = summary_data(ticker)
    if key_stats is None:
        return render_template("not_found.html", ticker=ticker, favorites=favorites)

    if key_stats:
        current_price = key_stats.pop("current_price")
    else:
        current_price = "N/A"

    sentiment = get_stock_sentiment(ticker)
    if sentiment:
        logo_url = sentiment["logo"]
        rating = sentiment["rating"]
        recommendation = "SELL" if rating == "Bullish" else "BUY"
    else:
        logo_url = ""
        recommendation = "N/A"

    name = full_name(ticker)

    chart = price_chart(ticker)

    c = MW(ticker)  # ticker is fine
    summary = c.get_summary()

    return render_template(
        "stock.html",
        name=name,
        ticker=ticker,
        logo_url=logo_url,
        current_price=current_price,
        recommendation=recommendation,
        key_stats=key_stats,
        summary=summary,
        chart=chart,
        favorites=favorites,
        is_favorite=is_favorite,
    )


@app.route("/favorite/<ticker>")
def favorite(ticker):
    """Favorites the given ticker if the user is logged in, redirects to
    login page if not."""
    if "username" not in session:
        return redirect(url_for("login"))

    add_favorite(get_user_id(session["username"]), ticker)
    return redirect(url_for("stock", ticker=ticker))


@app.route("/unfavorite/<ticker>")
def unfavorite(ticker):
    """Unfavorites the given ticker."""
    if "username" not in session:
        return redirect(url_for("stock", ticker=ticker))

    remove_favorite(get_user_id(session["username"]), ticker)
    return redirect(url_for("stock", ticker=ticker))


if __name__ == "__main__":
    app.debug = True
    app.run()
