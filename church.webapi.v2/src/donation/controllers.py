from flask import jsonify, Blueprint
from .services import create_donation, get_donations
from flask_login import login_required

donation_tb = Blueprint("donation", __name__)

@donation_tb.route("/donations", methods=["GET"])
def get_donation_route():
    try:
        return get_donations()
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@donation_tb.route("/donations", methods=["POST"])
def post_dontaion_route():
    try:
        return create_donation()
    except Exception as e:
        return jsonify({"error" : str(e)}), 500