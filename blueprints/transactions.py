from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update
from dbschema import db_engine, transactions_table, transaction_categories_table
from helpers.dates import date_to_html, validate_date
from helpers.currency import convert_money_input_to_db
from helpers.db_operations import remove_records_safely


transactions_bp = Blueprint("transactions_bp", __name__)

@transactions_bp.route("/transactions")
def transactions():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    with db_engine.begin() as conn:
        query = select(transactions_table, transaction_categories_table.c["name"]).join(
                transaction_categories_table,
                transaction_categories_table.c.id == transactions_table.c.category_id
            ).where(
                transactions_table.c.user_id == session["user_id"]
            )
        results = conn.execute(query)
    return render_template("transactions.html", results=results, has_date=True,
                           add_url="/transactions/forms/add", title="Transactions",
                           add_btn_txt="Add new transaction")


@transactions_bp.post("/transactions/remove")
def remove_transaction():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    ids = request.json["id"]
    if len(ids) == 0:
        return {"status" : "fail", "message" : "No rows selected"}
    
    if not remove_records_safely(ids, transactions_table, "id"):
        return {"status" : "fail", "message" : "An error has occurred"}
    return {"status" : "success", "message" : "Rows deleted successfully"}


@transactions_bp.route("/transactions/forms/add")
def add_transaction_form():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    with db_engine.begin() as conn:
        query = select(transaction_categories_table.c.name).where(
                transaction_categories_table.c.user_id == session["user_id"]
            )
        categories = conn.execute(query)
    return render_template("add_transaction.html", form_title="New Transaction", styles=["/static/transactions_form.css"], categories=categories, title="New Transaction")


@transactions_bp.post("/transactions/add")
def add_transaction():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    date = validate_date(request.form.get("date"))
    amount = convert_money_input_to_db(request.form.get("amount"))
    currency = request.form.get("currency")
    category = request.form.get("category")

    if not (date and amount != None and currency and category):
        return {"status" : "fail", "message" : "Blank fields"}
    if amount <= 0:
        return {"status" : "fail", "message" : "Non-positive amount"}
    if currency not in ["BRL", "USD", "EUR", "GBP"]:
        return {"status" : "fail", "message" : "Invalid currency"}
    
    with db_engine.begin() as conn:
        query = select(transaction_categories_table.c.id).where(
                and_(transaction_categories_table.c.user_id == session["user_id"],
                     transaction_categories_table.c.name == category)
            )
        results = conn.execute(query)
        if results.rowcount == 0:
            return {"status" : "fail", "message" : "Invalid category"}
        
    with db_engine.begin() as conn:
        query = insert(transactions_table).values(user_id=session["user_id"], amount=amount, date=date, currency=currency, category_id=results.first()[0])
        conn.execute(query)

    return {"status" : "success"}


@transactions_bp.post("/transactions/forms/update")
def update_transaction_form():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    id = request.form.get("id")
    date = date_to_html(request.form.get("date"))
    amount = request.form.get("amount")
    currency = request.form.get("currency")
    category_name = request.form.get("category_name")

    with db_engine.begin() as conn:
        query = select(transaction_categories_table.c.name).where(
                transaction_categories_table.c.user_id==session["user_id"]
            )
        categories = conn.execute(query)
    return render_template("update_transaction.html", title="Update Transaction", form_title="Update Transaction",
                           categories=categories, id=id, date=date, amount=amount, currency=currency, category_name=category_name,
                           styles=["/static/transactions_form.css"])


@transactions_bp.post("/transactions/update")
def update_transaction():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    id = request.form.get("id")
    date = validate_date(request.form.get("date"))
    amount = convert_money_input_to_db(request.form.get("amount"))
    currency = request.form.get("currency")
    category_name = request.form.get("category_name")

    if not (id and date and amount != None and currency and category_name):
        return {"status" : "fail", "message" : "Blank fields"}
    if amount <= 0:
        return {"status" : "fail", "message" : "Non positive amount"}
    if currency not in ["BRL", "USD", "EUR", "GBP"]:
        return {"status" : "fail", "message" : "Invalid currency"}
    
    with db_engine.begin() as conn:
        query = select(transaction_categories_table.c.id).where(
                and_(transaction_categories_table.c.user_id==session["user_id"],
                     transaction_categories_table.c.name==category_name)
            )
        category_id = conn.execute(query).scalar()
        if not category_id:
            return {"status" : "fail", "message" : "Invalid category"}
        
    with db_engine.begin() as conn:
        query = update(transactions_table).values(
                    amount=amount, date=date, currency=currency, category_id=category_id
                ).where(
                    and_(transactions_table.c.id == id, transactions_table.c.user_id==session["user_id"])
                )
        conn.execute(query)
    return {"status" : "success", "message" : "Transaction successfully added"}
