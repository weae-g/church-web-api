from flask import jsonify, Blueprint
from .services import (
    get_payment_note, get_payment_notes, create_payment_note, get_note_name, get_note_type,
    create_payment_note_type, update_payment_note_type, delete_payment_note_type,
    create_payment_note_name, update_payment_note_name, delete_payment_note_name,
    update_payment_note
)
from flask_login import login_required

note_tb = Blueprint("note", __name__)

@note_tb.route("/notes/<int:id>", methods=["GET"])
def get_payment_note_route(id):
    try:
        return get_payment_note(id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route('/update_payment_note/<int:payment_note_id>', methods=['PUT'])
def update_payment_note_route(payment_note_id):
    return update_payment_note(payment_note_id)

@note_tb.route("/notes/name", methods=["GET"])
def get_note_name_route():
    try:
        return get_note_name()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route("/notes/type", methods=["GET"])
def get_note_type_route():
    try:
        return get_note_type()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route("/notes", methods=["GET"])
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
        return jsonify({"error": str(e)}), 500

# PaymentNoteType Routes
@note_tb.route("note_types", methods=["POST"])
def create_payment_note_type_route():
    try:
        return create_payment_note_type()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route("/note_types/<int:note_type_id>", methods=["PUT"])
def update_payment_note_type_route(note_type_id):
    try:
        return update_payment_note_type(note_type_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route("/note_types/<int:note_type_id>", methods=["DELETE"])
def delete_payment_note_type_route(note_type_id):
    try:
        return delete_payment_note_type(note_type_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route("/note_names", methods=["POST"])
def create_payment_note_name_route():
    try:
        return create_payment_note_name()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route("/note_names/<int:note_name_id>", methods=["PUT"])
def update_payment_note_name_route(note_name_id):
    try:
        return update_payment_note_name(note_name_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@note_tb.route("/note_names/<int:note_name_id>", methods=["DELETE"])
def delete_payment_note_name_route(note_name_id):
    try:
        return delete_payment_note_name(note_name_id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

