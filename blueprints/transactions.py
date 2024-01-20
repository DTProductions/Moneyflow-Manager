from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update
from dbschema import db_engine, transactions_table, transaction_categories_table
from helpers.dates import html_date_to_db, db_date_to_html
from helpers.currency import convert_money_input_to_db
from helpers.db_operations import remove_records_safely


transactions_bp = Blueprint("transactions_bp", __name__)

@transactions_bp.route("/transactions")
def transactions():
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
    ids = request.json["id"]
    if len(ids) == 0:
        return {"status" : "fail", "message" : "No rows selected"}
    
    if not remove_records_safely(ids, transactions_table, "id"):
        return {"status" : "fail", "message" : "An error has occurred"}
    return {"status" : "success", "message" : "Rows deleted successfully"}


@transactions_bp.route("/transactions/forms/add")
def add_transaction_form():
    with db_engine.begin() as conn:
        query = select(transaction_categories_table.c.name).where(
                transaction_categories_table.c.user_id == session["user_id"]
            )
        categories = conn.execute(query)
    return render_template("add_transaction.html", form_title="Add new transaction", styles=["/static/transactions_form.css"], categories=categories)


@transactions_bp.post("/transactions/add")
def add_transaction():
    date = html_date_to_db(request.form.get("date"))
    ammount = convert_money_input_to_db(request.form.get("ammount"))
    currency = request.form.get("currency")
    category = request.form.get("category")

    if not (date and ammount and currency and category):
        return {"status" : "fail", "message" : "Blank fields"}
    if ammount <= 0:
        return {"status" : "fail", "message" : "Non-positive ammount"}
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
        query = insert(transactions_table).values(user_id=session["user_id"], ammount=ammount, date=date, currency=currency, category_id=results.first()[0])
        conn.execute(query)

    return {"status" : "success"}


@transactions_bp.post("/transactions/forms/update")
def update_transaction_form():
    id = request.form.get("id")
    date = db_date_to_html(request.form.get("date"))
    ammount = request.form.get("ammount")
    currency = request.form.get("currency")
    category_name = request.form.get("category_name")

    with db_engine.begin() as conn:
        query = select(transaction_categories_table.c.name).where(
                transaction_categories_table.c.user_id==session["user_id"]
            )
        categories = conn.execute(query)
    return render_template("update_transaction.html", title="Update transaction", form_title="Update transaction",
                           categories=categories, id=id, date=date, ammount=ammount, currency=currency, category_name=category_name,
                           styles=["/static/transactions_form.css"])


@transactions_bp.post("/transactions/update")
def update_transaction():
    id = request.form.get("id")
    date = html_date_to_db(request.form.get("date"))
    ammount = convert_money_input_to_db(request.form.get("ammount"))
    currency = request.form.get("currency")
    category_name = request.form.get("category_name")

    if not (id and date and ammount and currency and category_name):
        return {"status" : "fail", "message" : "Blank fields"}
    if ammount <= 0:
        return {"status" : "fail", "message" : "Non positive ammount"}
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
                    ammount=ammount, date=date, currency=currency, category_id=category_id
                ).where(
                    and_(transactions_table.c.id == id, transactions_table.c.user_id==session["user_id"])
                )
        conn.execute(query)
    return {"status" : "success", "message" : "Transaction successfully added"}
