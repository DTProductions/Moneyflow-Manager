from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import insert
from dbschema import db_engine, users_table
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
Session(app)

@app.route("/", )
def index():
    return render_template("login.html", page_title="login", form_title="Moneyflow Manager")

@app.route("/login", methods=["GET","POST"])
def login():
    return render_template("login.html", page_title="login", form_title="Moneyflow Manager")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not (email and password and confirmation):
            return "Blank fields"
        if email.count("@") != 1:
            return "Invalid email"
        if password != confirmation:
            return "Passwords didn't match"
        
        with db_engine.begin() as conn:
            query = insert(users_table).values(email=email, hash=generate_password_hash(password))
            conn.execute(query)
        return redirect("/")
    else:
        return render_template("register.html", page_title="register", form_title="Register")
