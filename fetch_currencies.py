from dbschema import historical_rates_table, db_engine
from sqlalchemy import insert
from datetime import datetime
from requests import get
from math import trunc

request_date = datetime.today().strftime("%Y-%m-%d")
request = get(f"https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/{request_date}/currencies/usd.json")
if request.status_code == 200:
    brl = trunc(float(request.json()["usd"]["brl"]) * 10**6)
    eur = trunc(float(request.json()["usd"]["eur"]) * 10**6)
    gbp = trunc(float(request.json()["usd"]["gbp"]) * 10**6)
    with db_engine.begin() as conn:
        query = insert(historical_rates_table).values(date=request_date, brl=brl, eur=eur, gbp=gbp)
        conn.execute(query)
        print("Successfully fetched currencies")
else:
    print("Failed fetch")
