from flask import Blueprint, request, session, redirect, render_template
from sqlalchemy import select, and_, or_
from dbschema import db_engine, transactions_table, transaction_categories_table, exchanges_table
from helpers.currency import format_money
from helpers.db_operations import safe_dict_increment, newest_historical_rate_date, oldest_historical_rate_date, get_closest_date_rates, dollar_based_conversion, sum_dict_values, get_used_currencies

overview_bp = Blueprint("overview_bp", __name__)


@overview_bp.route("/overview")
def overview():
    currencies = get_used_currencies()
    return render_template("overview.html", currencies=currencies)


@overview_bp.post("/overview")
def calculate_overview_values():
    selected_currency = request.json["selected_currency"]
    if not selected_currency:
        return {"status" : "fail", "message" : "Invalid currency"}
    
    selected_currency = selected_currency.split(" ")
    if selected_currency[0] not in get_used_currencies():
        return {"status" : "fail", "message" : "Invalid currency"}
    
    # single currency view
    if len(selected_currency) == 1:
        return single_view_data(selected_currency)
    
    # multicurrency view
    if len(selected_currency) == 2:
        if selected_currency[1] == "Total":
            multiview_data = calc_transactions_multiview(selected_currency[0])
            multiview_data["exchange_rate_impact"] = format_money(multiview_data["exchange_rate_impact"])
            format_totals(multiview_data)
            return multiview_data

    return {"status" : "fail", "message" : "Invalid currency"}


def single_view_data(selected_currency):
    single_view_data = calc_transactions_single_view(selected_currency[0])

    exchanges_data = calc_exchanges_single_view(selected_currency[0])

    single_view_data["total"] = single_view_data["total_income"] - single_view_data["total_expenses"] + exchanges_data["total_destination"] - exchanges_data["total_source"]

    format_totals(single_view_data)
    return single_view_data


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


def calc_transactions_multiview(selected_currency):
    with db_engine.begin() as conn:
        query = select(transactions_table.c["ammount", "currency", "date"], transaction_categories_table.c["name", "type"]).join(
                    transaction_categories_table,
                    transaction_categories_table.c.id == transactions_table.c.category_id
                ).where(
                    transactions_table.c.user_id == session["user_id"]
                )
        transactions = conn.execute(query)

        oldest_date_record = oldest_historical_rate_date()
        newest_date_record = newest_historical_rate_date()

        totals = {}

        income = {}
        expenses = {}
        for transaction in transactions:
            transaction = transaction._asdict()
            if transaction["type"] == "Income":
                if transaction["currency"] != selected_currency:
                    safe_dict_increment(totals, transaction["currency"], transaction["ammount"])
                    converted_ammount = get_converted_ammount(transaction["date"], transaction["currency"], transaction["ammount"], selected_currency, oldest_date_record, newest_date_record)                    
                    increment_incomes_forex(totals, income, transaction, converted_ammount)
                else:
                    safe_dict_increment(totals, transaction["currency"], transaction["ammount"])
                    increment_incomes_non_forex(totals, income, transaction, transaction["ammount"])

            # expenses
            elif transaction["currency"] != selected_currency:
                safe_dict_increment(totals, transaction["currency"], -transaction["ammount"])
                converted_ammount = get_converted_ammount(transaction["date"], transaction["currency"], transaction["ammount"], selected_currency, oldest_date_record, newest_date_record)                    
                increment_incomes_forex(totals, expenses, transaction, -converted_ammount)
            else:
                safe_dict_increment(totals, transaction["currency"], -transaction["ammount"])
                increment_incomes_non_forex(totals, expenses, transaction, -transaction["ammount"])

    exchange_totals = calc_exchanges_multiview()

    for currency in exchange_totals:
        if currency in totals:
            totals[currency] += exchange_totals[currency]
        else:
            totals[currency] = exchange_totals[currency]
    
    for currency in totals:
        if currency != selected_currency:
            converted_ammount = get_converted_ammount(newest_date_record["date"], currency, totals[currency], selected_currency, oldest_date_record, newest_date_record)
            totals[currency] = converted_ammount
    
    total = sum_dict_values(totals)

    total_income = sum_dict_values(income)
    total_expenses = sum_dict_values(expenses)
    total_expenses *= -1

    exchange_rate_impact = total - (total_income - total_expenses)

    format_money_values_dict(income)
    invert_value_signs(expenses)
    format_money_values_dict(expenses)

    return {"income_labels" : list(income.keys()), "income_data" : list(income.values()),
            "expenses_labels" : list(expenses.keys()), "expenses_data" : list(expenses.values()),
            "total_income" : total_income, "total_expenses" : total_expenses, "total" : total,
            "exchange_rate_impact" : exchange_rate_impact}


def increment_incomes_forex(totals, labels_dict, transaction, converted_ammount):
    safe_dict_increment(labels_dict, transaction["name"], converted_ammount)


def increment_incomes_non_forex(totals, labels_dict, transaction, value):
    safe_dict_increment(labels_dict, transaction["name"], value)


def get_converted_ammount(date, src_curr, ammount, dest_curr, oldest_date_record, newest_date_record):
    rates = get_closest_date_rates(date, oldest_date_record, newest_date_record)
    return dollar_based_conversion(src_curr, ammount, dest_curr, rates)


def format_money_values_dict(dictionary):
    for key in dictionary:
        dictionary[key] = format_money(dictionary[key])


def format_totals(view):
    view["total"] = format_money(view["total"])
    view["total_expenses"] = format_money(view["total_expenses"])
    view["total_income"] = format_money(view["total_income"])


def calc_exchanges_multiview():
    with db_engine.begin() as conn:
        query = select(exchanges_table).where(
                    and_(exchanges_table.c.user_id == session["user_id"])
                )
        exchanges = conn.execute(query)

        exchange_totals = {}

        for exchange in exchanges:
            exchange = exchange._asdict()
            safe_dict_increment(exchange_totals, exchange["source_currency"], -exchange["source_ammount"])
            safe_dict_increment(exchange_totals, exchange["destination_currency"], exchange["destination_ammount"])
    
    return exchange_totals


def invert_value_signs(dictionary):
    for key in dictionary:
        dictionary[key] *= -1
