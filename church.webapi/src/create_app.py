from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from config import config

# ----------------------------------------------- #

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_mode):
    app = Flask(__name__)    
    app.config.from_object(config[config_mode])
    login_manager.init_app(app)
    login_manager.login_view = "https://admin.spasskysobor.ru/admin/analitics"
    db.init_app(app)
    return app


# ----------------------------------------------- #
