from datetime import datetime
from create_app import db
from sqlalchemy import inspect
from sqlalchemy.orm import validates

class PaymentInfo(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Numeric, nullable=False)  # Используем Numeric для точности
    currency = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Дополнительные поля
    user_email = db.Column(db.String(255))
    from_name = db.Column(db.String(255))
    user_name = db.Column(db.String(255))
    phone_number = db.Column(db.String(50))
    note_cost = db.Column(db.String(255))
    note_name = db.Column(db.String(255))
    note_type = db.Column(db.String(255))
    donation = db.Column(db.String(255))
    type = db.Column(db.String(50))
    email_sent = db.Column(db.Boolean, default=False)
    email_sent_et2 = db.Column(db.Boolean, default=False)
    candle_type =db.Column(db.String(255))
    candle_icon = db.Column(db.String(255))
    candle_payer = db.Column(db.String(255))
    day = db.Column(db.String(255))


    def to_dict(self):
        return {
            'payment_id': self.payment_id,
            'amount': str(self.amount),  # Преобразуем Decimal в строку для JSON
            'currency': self.currency,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_email': self.user_email,
            'from_name': self.from_name,
            'user_name': self.user_name,
            'phone_number': self.phone_number,
            'note_cost': self.note_cost,
            'note_name': self.note_name,
            'note_type': self.note_type,
            'donation': self.donation,
            'type': self.type,
            'email_sent': self.email_sent,
            'email_sent_et2': self.email_sent_et2
        }
