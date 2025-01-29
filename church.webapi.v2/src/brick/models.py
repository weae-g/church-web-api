import uuid
from create_app import db
from datetime import datetime
class Brick(db.Model):
    __tablename__ = "tbbrick"
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.Text)
    message = db.Column(db.Text)
    cost=  db.Column(db.Numeric(precision=10, scale=2))
    color = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    mail = db.Column(db.Text)