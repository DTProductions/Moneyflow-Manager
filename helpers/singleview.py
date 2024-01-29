from dbschema import db_engine, transactions_table, transaction_categories_table, exchanges_table
from sqlalchemy import select, and_, or_
from flask import session
from helpers.dicts import safe_dict_increment
from helpers.currency import format_money_values_dict


def singleview_data(selected_currency):
    with db_engine.begin() as conn:
        query = select(transactions_table.c.amount, transaction_categories_table.c["name", "type"]).join(
                    transaction_categories_table,
                    transaction_categories_table.c.id == transactions_table.c.category_id
                ).where(
                    and_(transactions_table.c.user_id == session["user_id"],
                         transactions_table.c.currency == selected_currency)
                )
        transactions = conn.execute(query)

        income = {} # key is the name of the category, value is the amount
        expenses = {} # same as income
        total_income = 0
        total_expenses = 0

        for transaction in transactions:
            transaction = transaction._asdict()
            if transaction["type"] == "Income":
                total_income += transaction["amount"]
                safe_dict_increment(income, transaction["name"], transaction["amount"])
            else:
                total_expenses += transaction["amount"]
                safe_dict_increment(expenses, transaction["name"], transaction["amount"])

    format_money_values_dict(expenses)
    format_money_values_dict(income)

    total_exchanges = calc_exchanges_singleview(selected_currency)
    total = total_income - total_expenses + total_exchanges

    return {"income_labels" : list(income.keys()), "income_data" : list(income.values()),
            "expenses_labels" : list(expenses.keys()), "expenses_data" : list(expenses.values()),
            "total_income" : total_income, "total_expenses" : total_expenses, "total" : total}


def calc_exchanges_singleview(selected_currency):
    with db_engine.begin() as conn:
        query = select(exchanges_table).where(
                    and_(
                        exchanges_table.c.user_id == session["user_id"],
                        or_(exchanges_table.c.source_currency == selected_currency,
                            exchanges_table.c.destination_currency == selected_currency)
                    )
                )
        exchanges = conn.execute(query)

        total_exchanges = 0
        for exchange in exchanges:
            exchange = exchange._asdict()
            if exchange["source_currency"] == selected_currency:
                total_exchanges -= exchange["source_amount"]
            else:
                total_exchanges += exchange["destination_amount"]
    
    return total_exchanges
