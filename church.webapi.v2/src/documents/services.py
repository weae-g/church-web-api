from .models import Document, DocumentType
from .serialize import DocumentSchema
from flask import request, jsonify
import uuid, sys

sys.path.append(sys.path[0][:-9])
from create_app import db

DocumentSchemas = DocumentSchema(many=True)
DocumentSchemasOne = DocumentSchemas(many=False)

def get_all_documents():
    items = Document.query.all()
    response = DocumentSchemas.dump(items)
    return response

def get_all_documents_count():
    items = Document.query.all()
    response = DocumentSchemas.dump(items)
    return {"Количество: " : len(response)}

def get_document_by_type(type):
    items = (
        Document.query
        .filter(DocumentType.type_name == type)
        .all()
    )
    response = DocumentSchemas.dump(items)
    return response

def create_document():
    request_form = request.form.to_dict()
    id = str(uuid.uuid4())
    document = Document(
        document_id =  id,
        document_title = request_form["tbdocuments_title"],
        document_path = request_form["tbdocuments_path"],
        document_type_id = request_form["documents_type_id"],
    )
    db.session.add(document)
    db.session.commit()
    response = Document.query.get(id)
    return DocumentSchemasOne.dump(response)

def get_document_by_id(id):
    response = Document.query.get(id)
    if response:
        return DocumentSchemasOne.dump(response)
    else:
        return jsonify({"error" : f"Документа с иденификатором {id} не существует"})
    
def update_document_by_id(id):
    request_form = request.form.to_dict()
    item = Document.query.get(id)
    item.document_title = request_form["document_title"]
    item.document_path = request_form["document_path"]
    item.document_type_id = request_form["document_type_id"]
    db.session.commit()
    
    response = Document.query.get(id)
    return DocumentSchemasOne.dump(response)

def delete_document_by_id(id):
    Document.query.filter_by(document_id=id).delete()
    db.session.commit()
    
    return ('Документ с идентификатором "{}" успешно удалён').format(id)
 