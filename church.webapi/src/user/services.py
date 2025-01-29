from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify, Blueprint
from create_app import db
from .serialize import UsersSchema, UserRolesSchema, TbuserSchema
from .models import Users, UserRoles, Tbuser
from create_app import login_user, login_manager
import hashlib
from flask import session

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')
    session['cerf'] = 123
    if not login or not password:
        return jsonify({"message": "Логин и пароль обязательны"}), 400

    user = Users.query.join(Users.tbuser).filter(Tbuser.login == login).first()

    if not user:
        return jsonify({"message": "Пользователь с таким логином не найден"}), 404

    db.session.expunge_all()
    user = db.session.merge(user)
    
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    if user.tbuser.password == hashed_password:
        user_schema = UsersSchema().dump(user)
        login_user(user)
        session['user_id'] = user.tbuser.id
        return jsonify(user_schema), 200
    else:
        return jsonify({"message": "Неправильный пароль"}), 401

def get_user():
    users = Users.query.all()
    user_schema = UsersSchema(many=True).dump(users)
    return jsonify(user_schema), 200

def add_user():
    id = request.json['id']
    user_id = request.json['user_id']
    role_id = request.json['role_id']

    new_user = Users(id=id, user_id=user_id, role_id=role_id)

    try:
        db.session.add(new_user)
        db.session.commit()

        user_schema = UsersSchema().dump(new_user)
        return jsonify(user_schema), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Неудачная попытка создания нового пользователя', 'Детали': str(e)}), 500


def get_user_by_id():
    login = request.form.get('login')
    password_to_check = request.form.get('password_to_check')

    if not login or not password_to_check:
        return jsonify({"error": "Login and password_to_check are required"}), 400

    user = Users.query.join(Users.tbuser).filter(Tbuser.login == login).first()


    if user:
        tbuser = user.tbuser
        hashed_password = tbuser.password

        if check_password_hash(hashed_password, password_to_check):
            user_schema = UsersSchema().dump(user)
           
            return jsonify(user_schema), 200
            
    return jsonify({"error": "User not found or password is incorrect"}), 400

def is_valid_password(password):
    hashed_password = generate_password_hash(password, method='sha256')


    if check_password_hash(hashed_password, "wrong_password"):
        print("Пароль совпадает.")
    else:
        print("Пароль не совпадает.")
    
    return True