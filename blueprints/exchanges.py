from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update
from dbschema import db_engine, exchanges_table
from helpers.dates import date_to_html, validate_date
from helpers.currency import convert_money_input_to_db
from helpers.db_operations import remove_records_safely

exchanges_bp = Blueprint("exchanges_bp", __name__)


@exchanges_bp.route("/exchanges")
def exchanges():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    with db_engine.begin() as conn:
        query = select(exchanges_table).where(exchanges_table.c.user_id==session["user_id"])
        results = conn.execute(query)
    return render_template("exchanges.html", results=results, has_date=True,
                           add_url="/exchanges/forms/add", title="Exchanges",
                           add_btn_txt="Add new exchange")


@exchanges_bp.post("/exchanges/remove")
def remove_exchange():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    ids = request.json["id"]
    if len(ids) == 0:
        return {"status" : "fail", "message" : "No rows selected"}
    
    if not remove_records_safely(ids, exchanges_table, "id"):
        return {"status" : "fail", "message" : "An error has occurred"}
    return {"status" : "success", "message" : "Rows deleted successfully"}


@exchanges_bp.route("/exchanges/forms/add")
def add_exchange_form():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    return render_template("add_exchange.html", form_title="New Exchange", title="New Exchange", styles=["/static/exchanges_forms.css"])


@exchanges_bp.post("/exchanges/add")
def add_exchange():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    date = request.form.get("date")
    source_currency = request.form.get("source_currency")
    destination_currency = request.form.get("destination_currency")
    source_amount = convert_money_input_to_db(request.form.get("source_amount"))
    destination_amount = convert_money_input_to_db(request.form.get("destination_amount"))
    
    situation = validate_exchange_input(date, source_currency, destination_currency, source_amount, destination_amount)
    if situation["status"] == "fail":
        return situation
    
    with db_engine.begin() as conn:
        query = insert(exchanges_table).values(
                user_id=session["user_id"], source_currency=source_currency,
                source_amount=source_amount, destination_currency=destination_currency,
                destination_amount=destination_amount, date=date
            )
        conn.execute(query)

    return {"status" : "success", "message" : "Exchange successfully added"}


@exchanges_bp.post("/exchanges/forms/update")
def update_exchange_form():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    id = request.form.get("id")
    date = date_to_html(request.form.get("date"))
    source_amount = request.form.get("source_amount")
    source_currency = request.form.get("source_currency")
    destination_amount = request.form.get("destination_amount")
    destination_currency = request.form.get("destination_currency")
    return render_template("update_exchange.html", id=id, source_amount=source_amount,
                           source_currency=source_currency,destination_amount=destination_amount,
                           destination_currency=destination_currency, date=date, title="Update Exchange",
                           form_title="Update Exchange", styles=["/static/exchanges_forms.css"])


@exchanges_bp.post("/exchanges/update")
def update_exchange():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    id = request.form.get("id")
    date = request.form.get("date")
    source_amount = convert_money_input_to_db(request.form.get("source_amount"))
    source_currency = request.form.get("source_currency")
    destination_amount = convert_money_input_to_db(request.form.get("destination_amount"))
    destination_currency = request.form.get("destination_currency")

    situation = validate_exchange_input(date, source_currency, destination_currency, source_amount, destination_amount)
    if situation["status"] == "fail":
        return situation
    
    with db_engine.begin() as conn:
        query = update(exchanges_table).values(date=date, source_amount=source_amount,
                source_currency=source_currency, destination_amount=destination_amount,
                destination_currency=destination_currency).where(
                    and_(exchanges_table.c.user_id == session["user_id"], exchanges_table.c.id == id)
                )
        count = conn.execute(query).rowcount
        if count < 1:
            return {"status" : "fail", "message" : "An error has occured"}

    return {"status" : "success", "message" : "Exchange successfully updated"}


def validate_exchange_input(date, source_currency, destination_currency, source_amount, destination_amount):
    if not (source_currency and destination_currency and source_amount != None and destination_amount != None):
        return {"status" : "fail", "message" : "Blank fields"}
    if date:
        date = validate_date(date)
        if not date:
            return {"status" : "fail", "message" : "Invalid date"}
    if source_amount <= 0 or destination_amount <= 0:
        return {"status" : "fail", "message" : "Non-positive amount"}
    if not (destination_currency in ["BRL", "USD", "EUR", "GBP"] and source_currency in ["BRL", "USD", "EUR", "GBP"]):
        return {"status" : "fail", "message" : "Invalid currency"}
    return {"status" : "success"}
