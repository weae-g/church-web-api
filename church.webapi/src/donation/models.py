from create_app import db

class Donation(db.Model):
    __tablename__ = "tbdonation"
    payment_donation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donation_sum = db.Column(db.Numeric(precision=10, scale=2))    
    donation_name = db.Column(db.Text)
    description = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    mail = db.Column(db.Text)
