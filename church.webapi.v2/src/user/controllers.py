from flask import Blueprint, request, jsonify, current_app, session
from .models import UserRole, User
from .serialize import UserRoleSchema, UserSchema
from create_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

user_router = Blueprint('user_router', __name__)

# Роутер для создания нового пользователя
@user_router.route('/user', methods=['POST'])
def create_user():
    try:
        user_data = UserSchema().load(request.json)
        
        # Валидация входных данных
        hashed_password = generate_password_hash(user_data['password'])
        user_data['password'] = hashed_password
        
        # Создание нового пользователя
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        
        # Сериализация и отправка ответа
        serialized_user = UserSchema().dump(new_user)

        return jsonify(serialized_user), 201
    
    except ValidationError as ve:
        return jsonify({'error': ve.messages}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@user_router.route('/user/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@user_router.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            login = request.json.get('login')
            password = request.json.get('password')
            
            user = User.query.filter_by(login=login).first()
            if not user or not check_password_hash(user.password, password):
                return jsonify({'authorized': False}), 401

            login_user(user)
            return jsonify({'authorized': True}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': 'Please provide login credentials'}), 200

@user_router.route('/user/check', methods=['POST', 'GET'])
def check_user_existence_and_authenticate():
    if request.method == 'GET':
        return jsonify({'message': 'Please login'}), 200
    
    if request.method == 'POST':
        try:
            login = request.json.get('login')
            password = request.json.get('password')
            
            user = User.query.filter_by(login=login).first()
            if not user:
                return jsonify({'exists': False}), 200
            
            if not check_password_hash(user.password, password):
                return jsonify({'authorized': False}), 401

            login_user(user)
            
            user_schema = UserSchema()
            user_data = user_schema.dump(user)

            current_app.logger.info(f'User {user.login} authenticated')
            current_app.logger.info(f'Session: {session}')
            current_app.logger.info(f'Cookies: {request.cookies}')

            return jsonify({'user': user_data, 'authorized': True}), 200
        
        except Exception as e:
            current_app.logger.error(f'Error during authentication: {str(e)}')
            return jsonify({'error': str(e)}), 500

# Роутер для получения всех ролей в системе
@user_router.route('/user/roles', methods=['GET'])
@login_required
def get_all_roles():
    try:
        # Получаем все роли из базы данных
        roles = UserRole.query.all()
        
        # Сериализация и отправка ответа
        role_schema = UserRoleSchema(many=True)
        serialized_roles = role_schema.dump(roles)
        return jsonify(serialized_roles), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
