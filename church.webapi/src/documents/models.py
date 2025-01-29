from create_app import db

class Document(db.Model):
    __tablename__ = "tbdocuments"
    tbdocuments_id = db.Column(db.UUID, primary_key=True)
    tbdocuments_title = db.Column(db.Text)
    tbdocuments_path = db.Column(db.Text)
    documents_type_id =  db.Column(db.UUID, db.models.ForeignKey("documents_type.id"))
    documents_type = db.relationship(
        "DocumentType", backref=db.backref("documents_type", lazy="dynamic")
    )
    
class DocumentType(db.Model):
    __tablename__ = "documents_type"
    id = db.Column(db.UUID)
    type_name = db.Column(db.String())