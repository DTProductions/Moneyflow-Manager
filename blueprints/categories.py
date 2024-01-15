from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_
from dbschema import db_engine, transaction_categories_table
import json

categories_bp = Blueprint("categories_bp", __name__)

@categories_bp.route("/categories")
def categories():
    fields = ["Name", "Type"]
    with db_engine.begin() as conn:
        query = select(transaction_categories_table).where(transaction_categories_table.c.user_id == session["user_id"])
        results = conn.execute(query)
    return render_template("categories.html", results=results, fields=fields, title="Categories")


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


@categories_bp.route("/categories/forms/add")
def add_category_form():
    return render_template("add_category.html", title="New category", form_title="New Category")


@categories_bp.post("/categories/add")
def add():
    name = request.form.get("name")
    category_type = request.form.get("type")

    if category_type not in ["Income", "Expense"]:
        return {"status" : "fail", "message" : "Invalid type"}
    if not (name and category_type):
        return {"status" : "fail", "message" : "Blank fields"}
    
    with db_engine.begin() as conn:
        query = insert(transaction_categories_table).values(user_id=session["user_id"], type=category_type, name=name)
        conn.execute(query)
    return {"status" : "success", "message" : "Category successfully added"}
