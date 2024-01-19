from flask import Flask, redirect, session
from flask_session import Session
from datetime import timedelta
from blueprints.auth import login_bp, register_bp
from blueprints.overview import overview_bp
from blueprints.categories import categories_bp
from blueprints.transactions import transactions_bp
from helpers.currency import format_money

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
Session(app)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)

app.register_blueprint(overview_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(transactions_bp)

@app.context_processor
def utility_processor():
    return dict(format_money=format_money)

@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect("/login")
    else:
        return redirect("/overview")
    