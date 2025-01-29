from flask import Flask, request, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Замените на ваш секретный ключ

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Пример модели пользователя
class User(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

# Пример базы данных пользователей
users_db = {
    '1': User('1', 'user1', generate_password_hash('password1')),
    '2': User('2', 'user2', generate_password_hash('password2')),
}

@login_manager.user_loader
def load_user(user_id):
    return users_db.get(user_id)

# Маршрут для входа
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = [user for user in users_db.values() if user.username == username][0]
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Вход выполнен успешно'})
    return jsonify({'message': 'Ошибка аутентификации'}), 401

# Маршрут для выхода
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Выход выполнен успешно'})

# Защищенный маршрут
@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message': 'Это защищенный маршрут'})

if __name__ == '__main__':
    app.run()
