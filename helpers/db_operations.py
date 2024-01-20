from dbschema import db_engine
from sqlalchemy import delete, and_
from flask import session

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
