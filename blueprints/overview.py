from flask import Blueprint, request, render_template, session
from helpers.currency import format_money
from helpers.db_operations import get_used_currencies
from helpers.multiview import multiview_data
from helpers.singleview import singleview_data

overview_bp = Blueprint("overview_bp", __name__)


@overview_bp.route("/overview")
def overview():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")

    currencies = get_used_currencies()
    return render_template("overview.html", currencies=currencies)


@overview_bp.post("/overview")
def calculate_overview_values():
    if "user_id" not in session:
        return render_template("error.html", code=401, message="Unauthorized access")

    selected_currency = request.json["selected_currency"]
    if not selected_currency:
        return {"status" : "fail", "message" : "Invalid currency"}
    
    selected_currency = selected_currency.split(" ")
    if selected_currency[0] not in get_used_currencies():
        return {"status" : "fail", "message" : "Invalid currency"}
    
    # single currency view
    if len(selected_currency) == 1:
        view_data = singleview_data(selected_currency[0])
        format_totals(view_data)
        return view_data
    
    # multicurrency view
    if len(selected_currency) == 2:
        if selected_currency[1] == "Total":
            view_data = multiview_data(selected_currency[0])

            view_data["exchange_rate_impact"] = format_money(view_data["exchange_rate_impact"])
            format_totals(view_data)

            return view_data

    return {"status" : "fail", "message" : "Invalid currency"}


def format_totals(view):
    view["total"] = format_money(view["total"])
    view["total_expenses"] = format_money(view["total_expenses"])
    view["total_income"] = format_money(view["total_income"])
