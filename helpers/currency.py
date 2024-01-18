from math import trunc

db_digits = 4

# converts user input into a database-compliant monetary value
def convert_money_input_to_db(number):
    try:
        return trunc(float(number) * 10**db_digits)
    except:
        return None
    

# transform db money back into its original form
# NOTE: returns a string
def format_money(number):
    try:
        return "{:_.2f}".format(number / 10**db_digits).replace(".", ",").replace("_", ".")
    except:
        return None