from flask import request, jsonify, Blueprint
import sys

from .services import (
    get_all_documents,
    get_all_documents_count,
    get_document_by_id,
    get_document_by_type,
    create_document,
    update_document_by_id,
    delete_document_by_id
)

document_tb = Blueprint("documents", __name__)

@document_tb.route("/documents", methods=["GET"])
def get_documents_info():
    try:
        return get_all_documents(), 200
    except Exception as e:
        return e, 500

@document_tb.route("/documents/count", methods=["GET"])
def get_documents_count():
    try:
        return get_all_documents_count(), 200
    except Exception as e:
        return e, 500
    
@document_tb.route("/document/<uuid>", methods=["GET"])
def get_document_by_id(id):
    try:
        return get_document_by_id(id), 200
    except Exception as e:
        return e, 500
    
@document_tb.route("/document/<string>", methods=["GET"])
def get_documents_by_type(type):
    try:
        return get_document_by_type(type), 200
    except Exception as e:
        return e, 500
