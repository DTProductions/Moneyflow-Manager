from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update
from dbschema import db_engine, exchanges_table
from helpers.dates import html_date_to_db, db_date_to_html
from helpers.currency import convert_money_input_to_db
from helpers.db_operations import remove_records_safely

exchanges_bp = Blueprint("exchanges_bp", __name__)


@exchanges_bp.route("/exchanges")
def exchanges():
    with db_engine.begin() as conn:
        query = select(exchanges_table).where(exchanges_table.c.user_id==session["user_id"])
        results = conn.execute(query)
    return render_template("exchanges.html", results=results, has_date=True,
                           add_url="/exchanges/forms/add", title="Exchanges",
                           add_btn_txt="Add new exchange")


@exchanges_bp.post("/exchanges/remove")
def remove_exchange():
    ids = request.json["id"]
    if len(ids) == 0:
        return {"status" : "fail", "message" : "No rows selected"}
    
    if not remove_records_safely(ids, exchanges_table, "id"):
        return {"status" : "fail", "message" : "An error has occurred"}
    return {"status" : "success", "message" : "Rows deleted successfully"}
