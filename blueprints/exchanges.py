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


@exchanges_bp.route("/exchanges/forms/add")
def add_exchange_form():
    return render_template("add_exchange.html", form_title="New Exchange", title="New Exchange", styles=["/static/exchanges_forms.css"])


@exchanges_bp.post("/exchanges/add")
def add_exchange():
    date = html_date_to_db(request.form.get("date"))
    source_currency = request.form.get("source_currency")
    destination_currency = request.form.get("destination_currency")
    source_ammount = convert_money_input_to_db(request.form.get("source_ammount"))
    destination_ammount = convert_money_input_to_db(request.form.get("destination_ammount"))
    
    if not (date and source_currency and destination_currency and source_ammount != None and destination_ammount != None):
        return {"status" : "fail", "message" : "Blank fields"}
    
    if source_ammount <= 0 or destination_ammount <= 0:
        return {"status" : "fail", "message" : "Non-positive ammount"}
    if not (destination_currency in ["BRL", "USD", "EUR", "GBP"] and source_currency in ["BRL", "USD", "EUR", "GBP"]):
        return {"status" : "fail", "message" : "Invalid currency"}
    
    with db_engine.begin() as conn:
        query = insert(exchanges_table).values(
                user_id=session["user_id"], source_currency=source_currency,
                source_ammount=source_ammount, destination_currency=destination_currency,
                destination_ammount=destination_ammount, date=date
            )
        conn.execute(query)

    return {"status" : "success", "message" : "exchange successfully added"}
