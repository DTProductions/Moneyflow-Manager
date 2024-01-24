from math import trunc

db_digits = 4
rate_digits = 6

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
        return "{:,.2f}".format(number / 10**db_digits)
    except:
        return None


def dollar_based_conversion(src_curr, src_ammount, dest_curr, rates):
    src_curr = src_curr.lower()
    dest_curr = dest_curr.lower()
    
    if dest_curr == "usd":
        return trunc((src_ammount / rates[src_curr]) * 10 ** rate_digits)
    if src_curr == "usd":
        return trunc((src_ammount * rates[dest_curr]) / 10 ** rate_digits)
    
    src_to_dollar = trunc((src_ammount / rates[src_curr]) * 10 ** rate_digits)
    return trunc((src_to_dollar * rates[dest_curr]) / 10 ** rate_digits)


def format_money_values_dict(dictionary):
    for key in dictionary:
        dictionary[key] = "{:.2f}".format(dictionary[key] / 10**db_digits)
