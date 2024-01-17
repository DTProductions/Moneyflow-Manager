from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update
from dbschema import db_engine, transaction_categories_table

categories_bp = Blueprint("categories_bp", __name__)

@categories_bp.route("/categories")
def categories():
    with db_engine.begin() as conn:
        query = select(transaction_categories_table).where(transaction_categories_table.c.user_id == session["user_id"])
        results = conn.execute(query)
    return render_template("categories.html", results=results, title="Categories",
                           add_url="/categories/forms/add", has_date=False, add_btn_txt="Add new category")


@categories_bp.post("/categories/remove")
def remove_category():
    ids = request.json["id"]
    if len(ids) == 0:
        return {"status" : "fail", "message" : "No rows selected"}
    
    with db_engine.begin() as conn:
        query = delete(transaction_categories_table).where(
            and_(transaction_categories_table.c.id.in_(ids),
                 transaction_categories_table.c.user_id == session["user_id"])
        )
        deleted_rows_count = conn.execute(query).rowcount

        if deleted_rows_count != len(ids):
            conn.rollback()
            return {"status" : "fail", "message" : "An error has occurred"}

    return {"status" : "success", "message" : "Rows deleted successfully"}


@categories_bp.route("/categories/forms/add")
def add_category_form():
    return render_template("add_category.html", title="New category", form_title="New Category")


@categories_bp.post("/categories/add")
def add_category():
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


@categories_bp.post("/categories/forms/update")
def update_category_form():
    id = request.form.get("id")
    name = request.form.get("name")
    type = request.form.get("type")
    return render_template("update_category.html", id=id, name=name, category_type=type, title="Update Category", form_title="Update Category")


@categories_bp.post("/categories/update")
def update_category():
    id = request.form.get("id")
    name = request.form.get("name")
    category_type = request.form.get("type")

    if category_type not in ["Income", "Expense"]:
        return {"status" : "fail", "message" : "Invalid type"}
    if not (id and name and category_type):
        return {"status" : "fail", "message" : "Blank fields"}
    
    with db_engine.begin() as conn:
        query = update(transaction_categories_table).values(type=category_type, name=name).where(and_(transaction_categories_table.c.id == id, transaction_categories_table.c.user_id == session["user_id"]))
        updated_rows_count = conn.execute(query).rowcount

        if updated_rows_count == 0:
            return {"status" : "fail", "message" : "An error has occurred"}
        
    return {"status" : "success", "message" : "HA"}
