from datetime import datetime


# converts date from the YYYY-MM-DD format (used in html) into the DD/MM/YYYY format
# NOTE: "date" variable is a str
def format_db_date(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
        return date.strftime("%d/%m/%Y")
    except:
        return None


# converts a DD/MM/YYYY date into an html-compliant date(YYYY-MM-DD)
def date_to_html(date):
    try:
        date = datetime.strptime(date, "%d/%m/%Y")
        return date.strftime("%Y-%m-%d")
    except:
        return None


# makes sure date is formatted for the DB
def validate_date(date):
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except:
        return None
    