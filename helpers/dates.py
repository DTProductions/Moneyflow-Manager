from datetime import datetime

db_format = "%d/%m/%Y"

# converts date from the YYYY/MM/DD format (used in html) into the db format
# NOTE: "date" variable is a str
def html_date_to_db(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
        return date.strftime("%d/%m/%Y")
    except:
        return None


# converts a database-compliant date into an html-compliant date
def db_date_to_html(date):
    try:
        date = datetime.strptime(date, "%d/%m/%Y")
        return date.strftime("%Y-%m-%d")
    except:
        return None
