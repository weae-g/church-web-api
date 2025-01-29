import os
from flask import make_response

from flask_cors import CORS, cross_origin
from create_app import create_app as capp
from news.controllers import news_bp
from timetable.controllers import timetable_bp
from chatgpt.controllers import bot_bp
from gallery.controllers import gallery_bp
from employee.controllers import employee_bp
from smtp.controller import smtp_bp
from donation.controllers import donation_tb
from note.controllers import note_tb
from candle.controllers import candle_bp
from sacraments.controllers import sacraments_tb
from user.controllers import users_tb
#from documents.controllers import document_tb
from flask_session import Session




app = capp(os.getenv("CONFIG_MODE"))



UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True

secret_key = os.urandom(24)
app.config['SECRET_KEY'] = secret_key
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Настройте расширение Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # Используйте файловую систему для хранения сессий
app.config['SESSION_USE_SIGNER'] = True  # Используйте подпись для сессий
app.config['SESSION_PERMANENT'] = False  # Сессии будут храниться только во время активной сессии
app.config['SESSION_FILE_DIR'] = '/tmp/flask_session'  # Путь для хранения сессий
app.config['SESSION_KEY_PREFIX'] = 'my_session'  # Префикс для ключей сессий


# Инициализируйте расширение
Session(app)

CORS(app, supports_credentials=True, origins=["http://www.spasskysobor.ru", 
                   "https://www.spasskysobor.ru",
                   "http://www.spasskysobor.ru/", 
                   "https://www.spasskysobor.ru/",
                   "http://spasskysobor.ru", 
                   "https://spasskysobor.ru",
                   "http://admin.spasskysobor.ru",
                   "https://admin.spasskysobor.ru",
                   "http://admin.spasskysobor.ru/admin",
                   "https://admin.spasskysobor.ru/admin",
                   "http://127.0.0.1:5000",
                   "http://127.0.0.1:3000",
                   "http://localhost:3000",
                   "http://localhost:5000",
                   "http://localhost:5173"])


app.register_blueprint(news_bp, url_prefix="/api")
app.register_blueprint(timetable_bp, url_prefix="/api")
app.register_blueprint(bot_bp, url_prefix="/api")
app.register_blueprint(gallery_bp, url_prefix="/api")
app.register_blueprint(employee_bp, url_prefix="/api")
app.register_blueprint(smtp_bp, url_prefix="/api")
app.register_blueprint(donation_tb, url_prefix="/api")
app.register_blueprint(users_tb, url_prefix="/api")
app.register_blueprint(note_tb, url_prefix="/api")
app.register_blueprint(candle_bp, url_prefix="/api")

#app.register_blueprint(sacraments_tb, url_prefix="/api")



if __name__ == "__main__":
    app.run()
    