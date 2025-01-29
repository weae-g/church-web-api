from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from .tg_models import db, News  # замените на имя вашего приложения и модуль

# Функция для сохранения новости
def save_news_to_db(title, content):
    new_news = News(title=title, content=content)
    db.session.add(new_news)
    db.session.commit()

# Функция обработки сообщений от бота
def handle_message(update: Update, context: CallbackContext):
    message = update.message
    # Проверяем, что сообщение пришло из группы, где находится бот
    if message.chat.type == "group":
        title = message.caption if message.caption else ""
        content = message.text if message.text else ""
        save_news_to_db(title, content)
        message.reply_text('Новость успешно сохранена в базу данных!')

