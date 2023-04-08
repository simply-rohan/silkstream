import os

from flask import *

from dbclient import Directory

from snowflake import SnowflakeGenerator, Snowflake

from functools import wraps

app = Flask(__name__)  # Create the flask instance

# Secret key from `secrets.token_uslsafe()`. (e.g. Used to authenticate session)
app.secret_key = os.environ["SECRET_KEY"]

# Database setup

# Using .dbclient to manage local "db" folder
db = Directory(os.environ["DB_PATH"])


# Decorater to force user to login
def login_required(endpoint):
    @wraps(endpoint)
    def required_enpoint(*args, **kwargs):
        # Check if there is any user data in session
        if session.get("username") is None:
            return redirect(url_for("login"))

        # Check if user data is valid
        elif db["users"]["passwords"].get(session["username"]) is None:
            return redirect(url_for("login"))

        else:
            return endpoint(*args, **kwargs)

    return required_enpoint


# Home endpoint
@app.route("/")
@login_required
def home():
    return render_template("home.html")


# Auth ----


# Login endpoint and authenticater
@app.route("/auth/login", methods=["POST", "GET"])
@app.route("/auth/signin", methods=["POST", "GET"])
def login():
    if request.method == "GET": # Endpoint for login page
        errors = get_flashed_messages(category_filter=("error"))
        return render_template("auth/login.html", errors=errors)

    else: # Authenticator for login page
        username = request.form.get("username")
        password = request.form.get("password")

        if db["users"]["passwords"].get(username) == password:
            session["username"] = username

            return redirect(url_for("home"))

        else:
            flash("Incorrect username or password!", "error")
            return redirect(request.referrer)


# Registration endpoint and authenticator
@app.route("/auth/register", methods=["POST", "GET"])
@app.route("/auth/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET": # Endpoint for sign up page
        errors = get_flashed_messages(category_filter=("error"))
        return render_template("auth/signup.html", errors=errors)

    else: # Authenticator for sign up page
        username = request.form.get("username")
        password = request.form.get("password")

        if username not in db["users"]["passwords"].keys():
            # Create account
            file = db["users"]["passwords"]
            file[username] = password
            file.push()

            db["users"]["user_data"][username] = {
                "username": username,
                "profile": {"profile-picture": "guest.png", "bio": ""},
            }

            session["username"] = username # Log in user

            return redirect(url_for("home"))

        else:
            flash("Username already taken!", "error")
            return redirect(request.referrer)


# Utility endpoint to quickly logout user and return them to login page
@app.route("/auth/logout")
def logout():
    session["username"] = None
    return redirect(url_for("login"))
