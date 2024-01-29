from dbschema import db_engine, historical_rates_table, transactions_table, transaction_categories_table
from sqlalchemy import delete, and_, select, func
from flask import session
from datetime import datetime, timedelta
from math import trunc

# returns true if removal is allowed for the current user, false otherwise
def remove_records_safely(ids, table, id):
    with db_engine.begin() as conn:
        query = query = delete(table).where(
            and_(table.c[id].in_(ids), table.c.user_id == session["user_id"]))
        count = conn.execute(query).rowcount
        if len(ids) != count:
            conn.rollback()
            return False
        return True


def oldest_historical_rate_date():
    with db_engine.begin() as conn:
        query = select(func.min(historical_rates_table.c.date).label("date"), historical_rates_table.c["brl", "eur", "gbp"]).select_from(historical_rates_table)
        return conn.execute(query).first()._asdict()
    

def newest_historical_rate_date():
    with db_engine.begin() as conn:
        query = select(func.max(historical_rates_table.c.date).label("date"), historical_rates_table.c["brl", "eur", "gbp"]).select_from(historical_rates_table)
        return conn.execute(query).first()._asdict()
    

# This function will throw an infinite loop if there is no record in the historical rates tables, be sure to keep
# it filled!
def get_closest_date_rates(date, oldest_date_record, newest_date_record):
    offset = 1

    date_dt_time = datetime.strptime(date, "%Y-%m-%d")

    oldest_date = datetime.strptime(oldest_date_record["date"], "%Y-%m-%d")
    newest_date = datetime.strptime(newest_date_record["date"], "%Y-%m-%d")

    if date_dt_time <= oldest_date:
        return oldest_date_record
    elif date_dt_time >= newest_date:
        return newest_date_record

    while True:
        with db_engine.begin() as conn:
            query = select(func.count(), historical_rates_table).select_from(historical_rates_table).where(historical_rates_table.c.date == date)
            results = conn.execute(query).first()
            if results[0] == 1:
                return results._asdict()
            elif offset % 2 == 0:
                date_dt_time -= timedelta(days=offset)
            else:
                date_dt_time += timedelta(days=offset)
            date = date_dt_time.date().strftime("%Y-%m-%d")
            offset += 1

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
        return [row[0] for row in results]


def get_user_transactions():
    with db_engine.begin() as conn:
        query = select(transactions_table.c["amount", "currency", "date"], transaction_categories_table.c["name", "type"]).join(
                    transaction_categories_table,
                    transaction_categories_table.c.id == transactions_table.c.category_id
                ).where(
                    transactions_table.c.user_id == session["user_id"]
                )
        return conn.execute(query)
