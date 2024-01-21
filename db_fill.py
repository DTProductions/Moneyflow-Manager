from sqlalchemy import insert
from requests import get
from math import trunc
from datetime import datetime, timedelta
from dbschema import historical_rates_table, db_engine

current_date = datetime.today()
start_date = current_date - timedelta(days=180)

while start_date < current_date:
    request_date = start_date.date().strftime("%Y-%m-%d")
    request = get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{request_date}/currencies/usd.json")
    if request.status_code == 200:
        brl = trunc(float(request.json()["usd"]["brl"]) * 10**6)
        eur = trunc(float(request.json()["usd"]["eur"]) * 10**6)
        gbp = trunc(float(request.json()["usd"]["gbp"]) * 10**6)

        with db_engine.begin() as conn:
            query = insert(historical_rates_table).values(date=request_date, brl=brl, eur=eur, gbp=gbp)
            conn.execute(query)

    start_date += timedelta(days=1)
