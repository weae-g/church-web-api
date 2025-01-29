from flask import jsonify, Blueprint
from .services import get_payment_note, get_payment_notes, create_payment_note, get_note_name, get_note_type
from flask_login import login_required

note_tb = Blueprint("note", __name__)

@note_tb.route("/notes/<int:id>", methods=["GET"])
@login_required
def get_payment_note_route(id):
    try:
        return get_payment_note(id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@note_tb.route("/notes/name", methods=["GET"])
@login_required
def get_note_name_route():
    try:
        return get_note_name()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@note_tb.route("/notes/type", methods=["GET"])
@login_required
def get_note_type_route():
    try:
        return get_note_type()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route("/notes", methods=["GET"])
@login_required
def get_payment_notes_route():
    try:
        return get_payment_notes()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@note_tb.route("/notes", methods=["POST"])
def post_note_route():
    try:
        return create_payment_note()
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    
