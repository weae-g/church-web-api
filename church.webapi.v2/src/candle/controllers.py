

from flask import request, jsonify, Blueprint, Response, send_file
from flask_cors import CORS, cross_origin
from flask_login import login_required
from .services import (
    get_candle, create_candle, get_candle_all, get_icon, get_prayer, get_type,
    create_candle_prayer, update_candle_prayer,
    delete_candle_prayer, create_candle_icon, update_candle_icon, delete_candle_icon,
    create_candle_type, get_all_candle_types, get_candle_type, delete_candle_type, update_candle_type
)

candle_bp = Blueprint("candle", __name__)

#region candle_type
@candle_bp.route('/candle_types', methods=['POST'])
@login_required
def create_candle_type_router():
    return create_candle_type()

@candle_bp.route('/candle_types', methods=['GET'])
def get_all_candle_types_roter():
    return get_all_candle_types()

@candle_bp.route('/candle_types/<int:candle_type_id>', methods=['GET'])
def get_candle_type_router(candle_type_id):
    return get_candle_type(candle_type_id)

@candle_bp.route('/candle_types/<int:candle_type_id>', methods=['DELETE'])
@login_required
def delete_candle_type_router(candle_type_id):
    return delete_candle_type(candle_type_id)

@candle_bp.route('/candle_types/<int:candle_type_id>', methods=['PUT'])
@login_required
def update_candle_type_router(candle_type_id):
    return update_candle_type(candle_type_id)
#endregion

@candle_bp.route('/candle/icon_type')
def get_icon_route():
    try:
        return get_icon()
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle/prayer')
def get_prayer_route():
    try:
        return get_prayer()
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle/type')
def get_type_route():
    try:
        return get_type()
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle/<int:candle_id>', methods=['GET'])
def get_candle_route(candle_id):
    try:
        return get_candle(candle_id)
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle', methods=['GET'])
@login_required
def get_candle_all_route():
    try:
        return get_candle_all()
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle', methods=['POST'])
def create_candle_route():
    try:
        return create_candle()
    except Exception as e:
        return jsonify({"error": str(e)})

# Routes for CandlePrayer
@candle_bp.route('/candle_prayer', methods=['POST'])
@login_required
def create_candle_prayer_route():
    try:
        return create_candle_prayer()
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle_prayer/<int:prayer_id>', methods=['PUT'])
def update_candle_prayer_route(prayer_id):
    try:
        return update_candle_prayer(prayer_id)
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle_prayer/<int:prayer_id>', methods=['DELETE'])
@login_required
def delete_candle_prayer_route(prayer_id):
    try:
        return delete_candle_prayer(prayer_id)
    except Exception as e:
        return jsonify({"error": str(e)})

# Routes for CandelIcon
@candle_bp.route('/candle_icon', methods=['POST'])
@login_required
def create_candle_icon_route():
    try:
        return create_candle_icon()
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle_icon/<int:icon_id>', methods=['PUT'])
@login_required
def update_candle_icon_route(icon_id):
    try:
        return update_candle_icon(icon_id)
    except Exception as e:
        return jsonify({"error": str(e)})

@candle_bp.route('/candle_icon/<int:icon_id>', methods=['DELETE'])
@login_required
def delete_candle_icon_route(icon_id):
    try:
        return delete_candle_icon(icon_id)
    except Exception as e:
        return jsonify({"error": str(e)})