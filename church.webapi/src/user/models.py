from create_app import db
from flask_login import UserMixin
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.UUID, primary_key=True)
    user_id = db.Column(db.UUID, db.ForeignKey('tbuser.id'))
    role_id = db.Column(db.UUID, db.ForeignKey('user_roles.role_id'))
    tbuser = db.relationship('Tbuser', backref='users', foreign_keys=[user_id])
    user_roles = db.relationship('UserRoles', backref='users', foreign_keys=[role_id], uselist=True)
    
    def is_active(self):
        return self.active
class Tbuser(db.Model):
    __tablename__ = "tbuser"
    id = db.Column(db.UUID, primary_key=True)
    login = db.Column(db.Text)
    password = db.Column(db.Text)
    
class UserRoles(db.Model):
    __tablename__ = "user_roles"
    role_id = db.Column(db.UUID, primary_key=True)
    role = db.Column(db.Text)
