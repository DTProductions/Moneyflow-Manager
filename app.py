from flask import Flask, redirect, session
from flask_session import Session
from datetime import timedelta
from blueprints.auth import auth_bp
from blueprints.overview import overview_bp
from blueprints.categories import categories_bp
from blueprints.transactions import transactions_bp
from blueprints.exchanges import exchanges_bp
from helpers.currency import format_money
from helpers.dates import format_db_date

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)
Session(app)

app.register_blueprint(auth_bp)

app.register_blueprint(overview_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(exchanges_bp)

@app.context_processor
def utility_processor():
    return dict(format_money=format_money, format_db_date=format_db_date)

@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect("/login")
    else:
        return redirect("/overview")
    