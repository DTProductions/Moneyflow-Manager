from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update
from dbschema import db_engine, exchanges_table
from helpers.dates import html_date_to_db, db_date_to_html
from helpers.currency import convert_money_input_to_db

exchanges_bp = Blueprint("exchanges_bp", __name__)


@exchanges_bp.route("/exchanges")
def exchanges():
    with db_engine.begin() as conn:
        query = select(exchanges_table).where(exchanges_table.c.user_id==session["user_id"])
        results = conn.execute(query)
    return render_template("exchanges.html", results=results, has_date=True,
                           add_url="/exchanges/forms/add", title="Exchanges",
                           add_btn_txt="Add new exchange")