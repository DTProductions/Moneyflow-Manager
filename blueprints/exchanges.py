from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update
from dbschema import db_engine, exchanges_table
from helpers.dates import date_to_html, validate_date
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
    date = validate_date(request.form.get("date"))
    source_currency = request.form.get("source_currency")
    destination_currency = request.form.get("destination_currency")
    source_ammount = convert_money_input_to_db(request.form.get("source_ammount"))
    destination_ammount = convert_money_input_to_db(request.form.get("destination_ammount"))
    
    situation = validate_exchange_input(date, source_currency, destination_currency, source_ammount, destination_ammount)
    if situation["status"] == "fail":
        return situation
    
    with db_engine.begin() as conn:
        query = insert(exchanges_table).values(
                user_id=session["user_id"], source_currency=source_currency,
                source_ammount=source_ammount, destination_currency=destination_currency,
                destination_ammount=destination_ammount, date=date
            )
        conn.execute(query)

    return {"status" : "success", "message" : "Exchange successfully added"}


@exchanges_bp.post("/exchanges/forms/update")
def update_exchange_form():
    id = request.form.get("id")
    date = date_to_html(request.form.get("date"))
    source_ammount = request.form.get("source_ammount")
    source_currency = request.form.get("source_currency")
    destination_ammount = request.form.get("destination_ammount")
    destination_currency = request.form.get("destination_currency")
    return render_template("update_exchange.html", id=id, source_ammount=source_ammount,
                           source_currency=source_currency,destination_ammount=destination_ammount,
                           destination_currency=destination_currency, date=date, title="Update Exchange",
                           form_title="Update Exchange", styles=["/static/exchanges_forms.css"])


@exchanges_bp.post("/exchanges/update")
def update_exchange():
    id = request.form.get("id")
    date = validate_date(request.form.get("date"))
    source_ammount = convert_money_input_to_db(request.form.get("source_ammount"))
    source_currency = request.form.get("source_currency")
    destination_ammount = convert_money_input_to_db(request.form.get("destination_ammount"))
    destination_currency = request.form.get("destination_currency")

    situation = validate_exchange_input(date, source_currency, destination_currency, source_ammount, destination_ammount)
    if situation["status"] == "fail":
        return situation
    
    with db_engine.begin() as conn:
        query = update(exchanges_table).values(date=date, source_ammount=source_ammount,
                source_currency=source_currency, destination_ammount=destination_ammount,
                destination_currency=destination_currency).where(
                    and_(exchanges_table.c.user_id == session["user_id"], exchanges_table.c.id == id)
                )
        count = conn.execute(query).rowcount
        if count < 1:
            return {"status" : "fail", "message" : "An error has occured"}

    return {"status" : "success", "message" : "Exchange successfully updated"}


def validate_exchange_input(date, source_currency, destination_currency, source_ammount, destination_ammount):
    if not (date and source_currency and destination_currency and source_ammount != None and destination_ammount != None):
        return {"status" : "fail", "message" : "Blank fields"}
    if source_ammount <= 0 or destination_ammount <= 0:
        return {"status" : "fail", "message" : "Non-positive ammount"}
    if not (destination_currency in ["BRL", "USD", "EUR", "GBP"] and source_currency in ["BRL", "USD", "EUR", "GBP"]):
        return {"status" : "fail", "message" : "Invalid currency"}
    return {"status" : "success"}
