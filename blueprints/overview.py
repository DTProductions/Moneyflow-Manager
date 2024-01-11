from flask import Blueprint, request, session, redirect, render_template

overview_bp = Blueprint("overview_bp", __name__)

@overview_bp.route("/overview")
def overview():
    return render_template("overview.html")