from create_app import db
from marshmallow import Schema, fields

class PaymentNoteType(db.Model):
    __tablename__ = "tbpayment_note_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    cost = db.Column(db.Integer)    
    payment_note_names = db.relationship("PaymentNoteName", backref="payment_note_type")     


class PaymentNoteName(db.Model):
    __tablename__ = "tbpayment_note_name"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    id_type = db.Column(db.Integer, db.ForeignKey("tbpayment_note_type.id"))    


class PaymentNote(db.Model):
    __tablename__ = "tbpayment_note"
    tbpayment_note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tbpayment_note_type_id = db.Column(db.Integer, db.ForeignKey("tbpayment_note_type.id"))
    tbpayment_note_name_id = db.Column(db.Integer, db.ForeignKey("tbpayment_note_name.id"))
    author = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    to_name = db.Column(db.Text)
    
    payment_note_type = db.relationship("PaymentNoteType", backref="payment_notes")
    payment_note_name = db.relationship("PaymentNoteName", backref="payment_name")

