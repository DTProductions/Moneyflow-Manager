from flask import Blueprint, render_template, session, request
from sqlalchemy import select, delete, insert, and_, update, func
from dbschema import db_engine, transaction_categories_table, transactions_table
from helpers.db_operations import remove_records_safely

categories_bp = Blueprint("categories_bp", __name__)

@categories_bp.route("/categories")
def categories():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    with db_engine.begin() as conn:
        query = select(transaction_categories_table).where(transaction_categories_table.c.user_id == session["user_id"])
        results = conn.execute(query)
    return render_template("categories.html", results=results, title="Categories",
                           add_url="/categories/forms/add", has_date=False, add_btn_txt="Add new category")


@categories_bp.post("/categories/remove")
def remove_category():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    ids = request.json["id"]
    if len(ids) == 0:
        return {"status" : "fail", "message" : "No rows selected"}
    
    with db_engine.begin() as conn:
        query = select(func.count()).select_from(transactions_table).where(
                transactions_table.c.category_id.in_(ids)
            )
        count = conn.execute(query).scalar()
        if count > 0:
            return {"status" : "fail", "message" : "One of the selected categories is being used in a transaction"}
    
    if not remove_records_safely(ids, transaction_categories_table, "id"):
        return {"status" : "fail", "message" : "An error has occurred"}
    return {"status" : "success", "message" : "Rows deleted successfully"}


@categories_bp.route("/categories/forms/add")
def add_category_form():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    return render_template("add_category.html", title="New Category", form_title="New Category")


@categories_bp.post("/categories/add")
def add_category():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    name = request.form.get("name")
    category_type = request.form.get("type")

    if category_type not in ["Income", "Expense"]:
        return {"status" : "fail", "message" : "Invalid type"}
    if not (name and category_type):
        return {"status" : "fail", "message" : "Blank fields"}
    
    if exists_in_db(name):
        return {"status" : "fail", "message" : "Name already registered"}
    
    with db_engine.begin() as conn:
        query = insert(transaction_categories_table).values(user_id=session["user_id"], type=category_type, name=name)
        conn.execute(query)
    return {"status" : "success", "message" : "Category successfully added"}


@categories_bp.post("/categories/forms/update")
def update_category_form():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    id = request.form.get("id")
    name = request.form.get("name")
    type = request.form.get("type")
    return render_template("update_category.html", id=id, name=name, category_type=type, title="Update Category", form_title="Update Category")


@categories_bp.post("/categories/update")
def update_category():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")
    
    id = request.form.get("id")
    name = request.form.get("name")
    category_type = request.form.get("type")

    if category_type not in ["Income", "Expense"]:
        return {"status" : "fail", "message" : "Invalid type"}
    if not (id and name and category_type):
        return {"status" : "fail", "message" : "Blank fields"}
    
    if exists_in_db(name, id):
        return {"status" : "fail", "message" : "Name already registered"}
    
    with db_engine.begin() as conn:
        query = update(transaction_categories_table).values(type=category_type, name=name).where(and_(transaction_categories_table.c.id == id, transaction_categories_table.c.user_id == session["user_id"]))
        updated_rows_count = conn.execute(query).rowcount

        if updated_rows_count == 0:
            return {"status" : "fail", "message" : "An error has occurred"}
        
    return {"status" : "success", "message" : "Category successfully updated"}


def exists_in_db(name, id=-1):
    with db_engine.begin() as conn:
        query = select(func.count()).select_from(transaction_categories_table).where(
                and_(transaction_categories_table.c.user_id==session["user_id"], transaction_categories_table.c.name==name,
                     transaction_categories_table.c.id != id)
            )
        count = conn.execute(query).scalar()
        if count > 0:
            return True
        return False
