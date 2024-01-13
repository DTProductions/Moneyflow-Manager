from flask import Blueprint, render_template, session
from sqlalchemy import select
from dbschema import db_engine, transaction_categories_table

categories_bp = Blueprint("categories_bp", __name__)

@categories_bp.route("/categories")
def categories():
    fields = ["Name", "Type"]
    with db_engine.begin() as conn:
        query = select(transaction_categories_table).where(transaction_categories_table.c.user_id == session["user_id"])
        results = conn.execute(query)
    return render_template("categories.html", results=results, fields=fields)
