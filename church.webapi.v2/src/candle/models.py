from create_app import db
from datetime import datetime

class Candle(db.Model):
    __tablename__ = "tbpayment_candel"
    tbpayment_candel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tbpayment_candel_type_id = db.Column(db.Integer, db.ForeignKey('candel_type.id'))
    tbpayment_candel_icon = db.Column(db.Integer, db.ForeignKey('candel_icon.id'))
    tbpayment_candel_prayer = db.Column(db.Integer, db.ForeignKey('candel_prayer.id'))
    cost = db.Column(db.Numeric(precision=10, scale=2)) 
    day = db.Column(db.DateTime)
    to_name = db.Column(db.Text)
    author = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    finish = db.Column(db.Boolean, default=False)
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"))

    candle_type = db.relationship('CandleType', foreign_keys=[tbpayment_candel_type_id])
    candle_icon = db.relationship('CandelIcon', foreign_keys=[tbpayment_candel_icon])
    candle_prayer = db.relationship('CandlePrayer', foreign_keys=[tbpayment_candel_prayer])
    payment_info = db.relationship("PaymentInfo", backref="candles")

class CandleType(db.Model):
    __tablename__ = "candel_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    cost = db.Column(db.Numeric(precision=10, scale=2))

class CandlePrayer(db.Model):
    __tablename__ = "candel_prayer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    
class CandelIcon(db.Model):
    __tablename__ = "candel_icon"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
