from flask import *
from dbclient import Directory

app = Flask(__name__)
app.secret_key = "78268e16431fe604de3b3a246be77c02a856d01024b818bbb49405758c0ff26a"

db = Directory("silkstream/db")


@app.route("/")
def home():
    user_id = session.get("username")
    if user_id is None:
        return redirect(url_for("login"))

    return render_template("home.html")


# Auth ----


@app.route("/auth/login", methods=["POST", "GET"])
@app.route("/auth/signin", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        errors = get_flashed_messages(category_filter=("error"))
        return render_template("auth/login.html", errors=errors)

    else:
        username = request.form.get("username")
        password = request.form.get("password")

        if db["users"]["passwords"].get(username) == password:
            session["username"] = username

            return redirect(url_for("home"))

        else:
            flash("Incorrect username or password!", "error")
            return redirect(request.referrer)


@app.route("/auth/register", methods=["POST", "GET"])
@app.route("/auth/signup", methods=["POST", "GET"])
def signup():
    if request.method == "GET":
        errors = get_flashed_messages(category_filter=("error"))
        return render_template("auth/signup.html", errors=errors)

    else:
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

            session["username"] = username

            return redirect(url_for("home"))

        else:
            flash("Username already taken!", "error")
            return redirect(request.referrer)

@app.route("/auth/logout")
def logout():
    session["username"] = None