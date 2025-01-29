

from flask import request, jsonify, Blueprint, Response, send_file
from flask_cors import CORS, cross_origin
from flask_login import login_required
from .services import (
    get_all, create_brick, delete_brick
)

brick_bp = Blueprint("brick", __name__)

@brick_bp.route('/bricks')
def get_brick_route():
    try:
        return get_all()
    except Exception as e:
        return jsonify({"error": str(e)})

@brick_bp.route('/bricks', methods=['POST'])
def create_brick_router():
   return create_brick()

@brick_bp.route('/bricks/<uuid:id>', methods=['DELETE'])
@login_required
def delete_brick_router(id):
    return delete_brick(id=id)