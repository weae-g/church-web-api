from marshmallow import Schema, fields, ValidationError, pre_load


class DocumentTypeSchema(Schema):
    id = fields.UUID(dump_only=True)
    type_name = fields.Str()


class DocumentSchema(Schema):
    tbdocuments_id = fields.UUID(dump_only=True)
    documents_type = fields.Nested(DocumentTypeSchema)
    tbdocuments_title = fields.Str()
    tbdocuments_path = fields.Str()

