import os
import asyncio
from telethon import TelegramClient, events
from datetime import datetime
from io import BytesIO
from create_app import db
from .models import News, NewsImage
import base64

# Получение API токена бота из переменных окружения
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверка наличия переменной окружения с токеном
if not bot_token:
    raise ValueError("Telegram bot token not found in environment variables.")

# Создание клиента Telegram с использованием API токена бота
client = TelegramClient('session_name', api_id=None, api_hash=None, bot_token=bot_token)

async def save_image(message):
    """
    Сохранение изображения из сообщения в базу данных.
    """
    try:
        if message.photo:
            # Получаем файл фотографии
            file = await message.download_media(bytes)
            image_data = base64.b64encode(file).decode('utf-8')

            # Создание объекта NewsImage
            news_image = NewsImage(
                image_data=file,
                mimetype="image/jpeg",  # или другой формат
                name=message.photo.id
            )

            db.session.add(news_image)
            db.session.commit()
            return news_image.id
    except Exception as e:
        print(f"Ошибка при сохранении изображения: {e}")
        db.session.rollback()
    return None

async def add_news_to_db(event):
    """
    Функция для добавления новостей в базу данных.
    """
    try:
        message = event.message.message
        date = event.message.date

        # Сохранение изображения, если оно есть
        image_id = None
        if event.message.photo:
            image_id = await save_image(event.message)

        # Создание объекта News
        news = News(
            news_title=message[:100],  # Заголовок новости (ограничение до 100 символов)
            news_description=message,
            news_date=date,
            news_number=1  # Установите правильный номер новости, если необходимо
        )

        if image_id:
            news.news_image = [image_id]

        db.session.add(news)
        db.session.commit()
        print("Новость добавлена в базу данных.")
    except Exception as e:
        print(f"Ошибка при добавлении новости в базу данных: {e}")
        db.session.rollback()

@client.on(events.NewMessage(pattern='(?i)новость'))
async def handler(event):
    """
    Обработчик новых сообщений с ключевым словом 'новость'.
    """
    await add_news_to_db(event)

async def start_telegram_client():
    """
    Функция для запуска клиента Telegram.
    """
    await client.start()
    print("Telegram клиент запущен.")
    await client.run_until_disconnected()
