from waitress import serve
from app import app  # Замените "your_app" на ваш импорт Flask-приложения

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)  # Измените хост и порт по вашему выбору
