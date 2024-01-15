from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, RollbackToSavepointClause, and_
from dbschema import db_engine, transaction_categories_table
import json

categories_bp = Blueprint("categories_bp", __name__)

@categories_bp.route("/categories")
def categories():
    fields = ["Name", "Type"]
    with db_engine.begin() as conn:
        query = select(transaction_categories_table).where(transaction_categories_table.c.user_id == session["user_id"])
        results = conn.execute(query)
    return render_template("categories.html", results=results, fields=fields)

@categories_bp.post("/categories/remove")
def remove():
    ids = request.json["id"]
    if len(ids) == 0:
        return {"status" : "fail", "message" : "No rows selected"}
    
    with db_engine.begin() as conn:
        query = delete(transaction_categories_table).where(
            and_(transaction_categories_table.c.id.in_(ids),
                 transaction_categories_table.c.user_id == session["user_id"])
        )
        deleted_rows = conn.execute(query).rowcount

        if deleted_rows != len(ids):
            conn.rollback()
            return {"status" : "fail", "message" : "An error has occurred"}

    return {"status" : "success", "message" : "Rows deleted successfully"}