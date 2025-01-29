from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from prometheus_flask_exporter import PrometheusMetrics
import os
from datetime import timedelta
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_mode):
    app = Flask(__name__)
    app.config.from_object(config[config_mode])
    
    # Initialize Prometheus metrics
    metrics = PrometheusMetrics(app)

    # Initialize Flask-Login manager
    login_manager.init_app(app)
    login_manager.login_view = '/api/user/check'

    # Configure additional app settings
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Configure secret key
    app.secret_key = os.urandom(24)

    # Create session directory if it doesn't exist
    session_dir = '/tmp/flask_session'
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    # Configure Flask-Session extension
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_FILE_DIR'] = session_dir
    app.config['SESSION_KEY_PREFIX'] = 'my_session'

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=False  # Установите True, если используете HTTPS
    )

    Session.permanent = True
    Session(app)

    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

    # Initialize SQLAlchemy
    db.init_app(app)

    return app, db, login_manager
