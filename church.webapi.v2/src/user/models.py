import uuid
from create_app import db
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

class UserRole(db.Model):
    __tablename__ = 'user_roles'

    role_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    role = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<UserRole role_id={self.role_id}, role={self.role}>'
    
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    role_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('user_roles.role_id'), nullable=False)
    login = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    role = relationship('UserRole', backref='users')

    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User id={self.id}, login={self.login}>'

    def is_authenticated(self):
        # Пользователь считается авторизованным, если он прошел аутентификацию и аккаунт активен
        return True

    def is_active(self):
        # Пользователь считается активным, если аккаунт не деактивирован
        return True

    def is_anonymous(self):
        # В данном примере не используется анонимный пользователь
        return False

    def get_id(self):
        # Возвращаем строковое представление id пользователя
        return str(self.id)