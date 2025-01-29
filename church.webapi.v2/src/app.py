import os
from flask import Flask
from flask_cors import CORS

from create_app import create_app
from news.controllers import news_bp
from brick.controllers import brick_bp
from timetable.controllers import timetable_bp
from chatgpt.controllers import bot_bp
from gallery.controllers import gallery_bp
from employee.controllers import employee_bp
from donation.controllers import donation_tb
from note.controllers import note_tb
from candle.controllers import candle_bp
from sacraments.controllers import sacraments_tb
from user.controllers import user_router
from payment.services import payment_bp


from flask import Flask, request, jsonify


# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Create Flask app using create_app function
app, db, login_manager = create_app(os.getenv("CONFIG_MODE", "staging"))  

# Configure CORS
CORS(app, supports_credentials=True, resources={r"/*": {"origins": [
    "http://www.spasskysobor.ru",
    "https://www.spasskysobor.ru",
    "http://spasskysobor.ru",
    "https://spasskysobor.ru",
    "http://admin.spasskysobor.ru",
    "https://admin.spasskysobor.ru",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:5173",
    "https://yoomoney.ru",
    "https://yourdomain.com/payment_success"
]}}, headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])



# Register blueprints


app.register_blueprint(news_bp, url_prefix="/api")
app.register_blueprint(timetable_bp, url_prefix="/api")
app.register_blueprint(bot_bp, url_prefix="/api")
app.register_blueprint(gallery_bp, url_prefix="/api")
app.register_blueprint(employee_bp, url_prefix="/api")
app.register_blueprint(donation_tb, url_prefix="/api")
app.register_blueprint(note_tb, url_prefix="/api")
app.register_blueprint(candle_bp, url_prefix="/api")
app.register_blueprint(user_router, url_prefix="/api")
app.register_blueprint(brick_bp, url_prefix="/api")
app.register_blueprint(payment_bp, url_prefix="/api")



# Uncomment if needed
# app.register_blueprint(sacraments_tb, url_prefix="/api")



if __name__ == "__main__":
    

    app.run()
