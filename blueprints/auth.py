from flask import Blueprint, request, session, redirect, render_template
from sqlalchemy import insert, select, func
from werkzeug.security import generate_password_hash, check_password_hash
from dbschema import db_engine, users_table


auth_bp = Blueprint("auth_bp", __name__)
@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not (email and password):
            return render_template("error.html", code=400, message="Blank fields")
        
        with db_engine.begin() as conn:
            query = select(users_table.c["id","hash"]).where(users_table.c.email == email)
            result = conn.execute(query)
            result = result.first()

            if not result:
                return render_template("error.html", code=400, message="Email not registered")
            if not check_password_hash(result[1], password):
                return render_template("error.html", code=400, message="Wrong password")
            
            session["user_id"] = result[0]
            return redirect("/")
    else:    
        return render_template("login.html", page_title="login", form_title="Moneyflow Manager")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not (email and password and confirmation):
            return render_template("error.html", code=400, message="Blank fields")
        if email.count("@") != 1:
            return render_template("error.html", code=400, message="Invalid email")
        if password != confirmation:
            return render_template("error.html", code=400, message="Passwords didn't match")

        with db_engine.begin() as conn:
            query = select(func.count("*")).select_from(users_table).where(users_table.c.email == email)
            count = conn.execute(query).scalar()
            if count > 0:
                return render_template("error.html", code=400, message="Email already registered")

        with db_engine.begin() as conn:
            query = insert(users_table).values(email=email, hash=generate_password_hash(password))
            conn.execute(query)
        return redirect("/login")
    else:
        return render_template("register.html", page_title="register", form_title="Register")
    