from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update
from dbschema import db_engine, transactions_table, transaction_categories_table


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
    
    with db_engine.begin() as conn:
        query = delete(transactions_table).where(
            and_(transactions_table.c.id.in_(ids), transactions_table.c.user_id == session["user_id"]))

        deleted_rows_count = conn.execute(query).rowcount
        if len(ids) != deleted_rows_count:
            conn.rollback()
            return {"status" : "fail", "message" : "An error has occurred"}
        
    return {"status" : "success", "message" : "Rows deleted successfully"}
