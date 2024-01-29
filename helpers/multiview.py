from helpers.dicts import safe_dict_increment, sum_dict_values, invert_value_signs
from helpers.currency import dollar_based_conversion, format_money_values_dict
from helpers.db_operations import get_closest_date_rates, oldest_historical_rate_date, newest_historical_rate_date, get_user_transactions
from dbschema import db_engine, exchanges_table
from sqlalchemy import select, and_
from flask import session


def multiview_data(selected_currency):
    transactions = get_user_transactions()

    totals = {}
    income = {}
    expenses = {}

    oldest_date_record = oldest_historical_rate_date()
    newest_date_record = newest_historical_rate_date()
    for transaction in transactions:
        transaction = transaction._asdict()
        if transaction["type"] == "Income":
            add_transaction_data_to_dicts(transaction, totals, income, oldest_date_record,
                                          newest_date_record, selected_currency, transaction["amount"])
        else:
            # expenses
            add_transaction_data_to_dicts(transaction, totals, expenses, oldest_date_record,
                                          newest_date_record, selected_currency, -transaction["amount"])

    exchange_totals = calc_exchanges_multiview()
    add_exchanges_to_totals(totals, exchange_totals)

    calc_rates_totals(totals, selected_currency, newest_date_record, oldest_date_record)
    
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


def add_transaction_data_to_dicts(transaction, totals, income_expenses_dict, oldest_date_record, newest_date_record, selected_currency, amount):
    if transaction["currency"] != selected_currency:
        safe_dict_increment(totals, transaction["currency"], amount)
        
        converted_amount = get_converted_amount(transaction["date"], transaction["currency"],
                                                  amount, selected_currency, oldest_date_record,
                                                  newest_date_record)
        
        safe_dict_increment(income_expenses_dict, transaction["name"], converted_amount)
    else:
        safe_dict_increment(totals, transaction["currency"], amount)
        safe_dict_increment(income_expenses_dict, transaction["name"], amount)


def get_converted_amount(date, src_curr, amount, dest_curr, oldest_date_record, newest_date_record):
    rates = get_closest_date_rates(date, oldest_date_record, newest_date_record)
    return dollar_based_conversion(src_curr, amount, dest_curr, rates)


def add_exchanges_to_totals(totals, exchange_totals):
    for currency in exchange_totals:
        if currency in totals:
            totals[currency] += exchange_totals[currency]
        else:
            totals[currency] = exchange_totals[currency]


def calc_rates_totals(totals, selected_currency, newest_date_record, oldest_date_record):
    for currency in totals:
        if currency != selected_currency:
            converted_amount = get_converted_amount(newest_date_record["date"], currency, totals[currency],
                                                      selected_currency, oldest_date_record, newest_date_record)
            totals[currency] = converted_amount


def calc_exchanges_multiview():
    with db_engine.begin() as conn:
        query = select(exchanges_table).where(
                    and_(exchanges_table.c.user_id == session["user_id"])
                )
        exchanges = conn.execute(query)

        exchange_totals = {}

        for exchange in exchanges:
            exchange = exchange._asdict()
            safe_dict_increment(exchange_totals, exchange["source_currency"], -exchange["source_amount"])
            safe_dict_increment(exchange_totals, exchange["destination_currency"], exchange["destination_amount"])
    
    return exchange_totals
