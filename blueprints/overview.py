from flask import Blueprint, request, session, redirect, render_template
from sqlalchemy import select, and_, or_
from dbschema import db_engine, transactions_table, transaction_categories_table, exchanges_table
from helpers.currency import format_money
from helpers.db_operations import safe_dict_increment

overview_bp = Blueprint("overview_bp", __name__)

@overview_bp.route("/overview")
def overview():
    currencies = get_used_currencies()
    return render_template("overview.html", currencies=currencies)


# optimized SQL query for finding which currencies the user has transacted in
def get_used_currencies():
    with db_engine.begin() as conn:
        query = select(transactions_table.c.currency).where(
                    transactions_table.c.id.in_(
                        select(transactions_table.c.id).where(
                                and_(transactions_table.c.user_id == session["user_id"],
                                     transactions_table.c.currency == "BRL")
                        ).limit(1)
                    ).__or__(
                        transactions_table.c.id.in_(
                            select(transactions_table.c.id).where(
                                and_(transactions_table.c.user_id == session["user_id"],
                                     transactions_table.c.currency == "USD")
                            ).limit(1)
                        )
                    ).__or__(
                        transactions_table.c.id.in_(
                            select(transactions_table.c.id).where(
                                and_(transactions_table.c.user_id == session["user_id"],
                                     transactions_table.c.currency == "EUR")
                            ).limit(1)
                        )
                    ).__or__(
                        transactions_table.c.id.in_(
                            select(transactions_table.c.id).where(
                                and_(transactions_table.c.user_id == session["user_id"],
                                     transactions_table.c.currency == "GBP")
                            ).limit(1)
                        )
                    )
                )
        results = conn.execute(query)
        currencies = [row[0] for row in results]
        return currencies
    

@overview_bp.post("/overview")
def calculate_overview_values():
    selected_currency = request.json["selected_currency"]
    if not selected_currency:
        return {"status" : "fail", "message" : "Invalid currency"}
    
    selected_currency = selected_currency.split(" ")
    if selected_currency[0] not in get_used_currencies():
        return {"status" : "fail", "message" : "Invalid currency"}
    
    # view for single currency
    if len(selected_currency) == 1:
        single_view_data = calc_transactions_single_view(selected_currency[0])

        exchanges_data = calc_exchanges_single_view(selected_currency[0])

        single_view_data["total"] = single_view_data["total_income"] - single_view_data["total_expenses"] + exchanges_data["total_destination"] - exchanges_data["total_source"]

        single_view_data["total"] = format_money(single_view_data["total"])
        single_view_data["total_expenses"] = format_money(single_view_data["total_expenses"])
        single_view_data["total_income"] = format_money(single_view_data["total_income"])
        return single_view_data
    
    if len(selected_currency) == 2:
        if selected_currency[1] == "Total":
            print("Multiview")
        else:
            return {"status" : "fail", "message" : "Invalid currency"}
    return {"status" : "fail", "message" : "Invalid currency"}


def calc_transactions_single_view(selected_currency):
    with db_engine.begin() as conn:
        query = select(transactions_table.c.ammount, transaction_categories_table.c["name", "type"]).join(
                    transaction_categories_table,
                    transaction_categories_table.c.id == transactions_table.c.category_id
                ).where(
                    and_(transactions_table.c.user_id == session["user_id"],
                         transactions_table.c.currency == selected_currency)
                )
        transactions = conn.execute(query)

        income = {} # key is the name of the category, value is the ammount
        expenses = {} # same as income
        total_income = 0
        total_expenses = 0

        for transaction in transactions:
            transaction = transaction._asdict()
            if transaction["type"] == "Income":
                total_income += transaction["ammount"]
                safe_dict_increment(income, transaction["name"], transaction["ammount"])
            else:
                total_expenses += transaction["ammount"]
                safe_dict_increment(expenses, transaction["name"], transaction["ammount"])

    for category in expenses:
        expenses[category] = format_money(expenses[category])
    for category in income:
        income[category] = format_money(income[category])

    return {"income_labels" : list(income.keys()), "income_data" : list(income.values()),
            "expenses_labels" : list(expenses.keys()), "expenses_data" : list(expenses.values()),
            "total_income" : total_income, "total_expenses" : total_expenses}


def calc_exchanges_single_view(selected_currency):
    with db_engine.begin() as conn:
        query = select(exchanges_table).where(
                    and_(
                        exchanges_table.c.user_id == session["user_id"],
                        or_(exchanges_table.c.source_currency == selected_currency,
                            exchanges_table.c.destination_currency == selected_currency)
                    )
                )
        exchanges = conn.execute(query)

        total_source = 0
        total_destination = 0
        for exchange in exchanges:
            exchange = exchange._asdict()
            if exchange["source_currency"] == selected_currency:
                total_source += exchange["source_ammount"]
            else:
                total_destination += exchange["destination_ammount"]
    
    return {"total_source" : total_source, "total_destination" : total_destination}
