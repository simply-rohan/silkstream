from flask import *
from dbclient import Directory

app = Flask(__name__)
app.secret_key = "k2wG|b+3Tf)KboN1K)EYEOMu.q[?"

db = Directory("silkstream/db")


@app.route("/")
def home():
    user_id = session.get("username")
    if user_id is None:
        return redirect("/login")
    return render_template("home.html")


# Auth ----


@app.route("/login", methods=["POST", "GET"])
@app.route("/signin")
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")


        if db["users"]["passwords"].get(username) == password:
            session["username"] = username
        
        return redirect(url_for('home'))


@app.route("/register")
@app.route("/signup")
def signup():
    return render_template("auth/signup.html")
