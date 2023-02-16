import os

from settingDB import notion, engine
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')
datetime.now(JST)
# engine = create_engine("sqlite:///application.db", echo=True)

Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

# Configure application
app = Flask(__name__)
session = Session()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///application.db")

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO",200)
    # render_template('portforio.html')


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbolData = lookup(request.form.get("Symbol"))

        # シンボルがなかったら400を返す
        if lookup(request.form.get("Symbol")) is None:
            return apology("must provide username", 400)

        # 正の整数の株を買う
        if not request.form.get("shares"):
            return apology("must provide username", 400)

        # 所持金額を調べて持っていれば購入しよう
        # hadCash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
        # payment = symbolData["price"] * request.form.get("shares")
        # if hadCash >= payment:
        #     db.execute("UPDATE user SET cash=? WHERE username=?", hadCash - payment, session["user_id"])
        # else:
        #     return apology("faild buying", 400)

        flash("bought!")
        return redirect("/")

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    # session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        # rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        # if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
        #     return apology("invalid username and/or password", 403)

        # # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        # シンボルが空白だったら400を返す
        if not request.form.get("Symbol"):
            return apology("must provide username", 400)

        # シンボルがないやつは400を返す
        symbolData = lookup(request.form.get("Symbol"))
        if symbolData is None:
            return apology("INVALID SYMBOL", 400)

        name = request.form.get(symbolData["name"])
        symbol = request.form.get(symbolData["Symbol"])
        price = request.form.get(symbolData["price"])

        # シンボルが正常であったら表示できるようにする　お金返す？======================================================
        return render_template("quoted.html" ,name=name ,Symbol=symbol ,price=usd(price))

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # パスワードの再入力が一致しているか
        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("invalid username and/or password", 400)

        # # すでにユーザー名が使われていないか
        # elif len(rows) :
        #     return apology("invalid username and/or password", 400)

        # # Query database for username
        # hash = generate_password_hash(request.form.get("password"))
        # user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)" ,request.form.get("username") ,hash)

        # session["user_id"] = user_id

        flash("registered!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":



        return redirect("/")

    else:
        return render_template("sell.html")
