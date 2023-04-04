from flask import *

app = Flask(__name__)

@app.route("/")
def home():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect("/login")
    return render_template("home.html")

# Auth ----

@app.route("/login")
@app.route("/signin")
def login():
    return render_template("auth/login.html")

@app.route("/register")
@app.route("/signup")
def signup():
    return render_template("auth/signup.html")

@app.route("/validate_login")
def validate_login():
    pass