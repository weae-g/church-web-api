workers = 4  # Количество рабочих процессов
bind = "127.0.0.1:5000"  # Хост и порт, на котором будет слушать Gunicorn

# Имя модуля и объекта приложения Flask
module = "app:app"  # Здесь "app" - имя модуля, "app" - имя объекта приложения Flask

# Конфигурация Flask-Session
raw_env = [
    "SESSION_TYPE=filesystem",
    "SESSION_USE_SIGNER=True",
    "SESSION_PERMANENT=False",
    "SESSION_FILE_DIR=/tmp/flask_session",
    "SESSION_KEY_PREFIX=my_session",
]
