from flask import jsonify, Blueprint, request
from flask_login import login_required, logout_user
from .services import add_user, get_user_by_id, get_user, login

users_tb = Blueprint("user_login", __name__)

@users_tb.route('users/login', methods=['POST'])
def login_route():
    try:
        return login()
    except Exception as e:
        return jsonify({"error" : str(e)})


@users_tb.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Выход выполнен успешно'})

@users_tb.route('/users/06b7c823-d7a9-4a4e-a12d-3383edb116d9', methods=['GET'])
def get_user_route():
    try:
        return get_user()
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@users_tb.route('/users', methods=['POST'])
def add_user_route():
    try:
        return add_user()
    except Exception as e:
        return jsonify({"error" : str(e)})
        
@users_tb.route('/users_login', methods=["POST"])
def users_by_id_route():
    try:
        return get_user_by_id()
    except Exception as e:
        return jsonify({"error" : str(e)})