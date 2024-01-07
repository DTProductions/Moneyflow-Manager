from sqlalchemy import create_engine, MetaData

db_engine = create_engine("sqlite+pysqlite:///moneyflow_manager.db")

db_metadata = MetaData()
db_metadata.reflect(bind=db_engine)

#initialize Table objects
historical_rates_table = db_metadata.tables["historical_rates"]
exchanges_table = db_metadata.tables["exchanges"]
transaction_categories_table = db_metadata.tables["transaction_categories"]
transactions_table = db_metadata.tables["transactions"]
users_table = db_metadata.tables["users"]