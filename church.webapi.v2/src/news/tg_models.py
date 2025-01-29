import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from create_app import db, app  # относительный импорт
from sqlalchemy.orm import validates

class News(db.Model):
    __tablename__ = "tg_news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    @staticmethod
    def save_news(title, content, photo_url=None):
        new_news = News(title=title, content=content, photo_url=photo_url)
        db.session.add(new_news)
        db.session.commit()
        return new_news

    @staticmethod
    def update_news(news_id, title=None, content=None, photo_url=None):
        news = News.query.get(news_id)
        if news:
            if title:
                news.title = title
            if content:
                news.content = content
            if photo_url:
                news.photo_url = photo_url
            db.session.commit()
            return news
        return None

    @staticmethod
    def delete_news(news_id):
        news = News.query.get(news_id)
        if news:
            db.session.delete(news)
            db.session.commit()
            return True
        return False

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 255:
            raise ValueError("Title cannot be longer than 255 characters")
        return title

    @validates('photo_url')
    def validate_photo_url(self, key, photo_url):
        if photo_url and len(photo_url) > 255:
            raise ValueError("Photo URL cannot be longer than 255 characters")
        return photo_url

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Замените на ваш chat ID
GROUP_CHAT_ID = -1001769191205  # ваш chat_id

# Функция для обработки текстовых сообщений в группе
def handle_group_message(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id != GROUP_CHAT_ID:
        return  # игнорируем сообщения из других чатов

    text = update.message.text
    try:
        title, content = text.split('\n', 1)
    except ValueError:
        update.message.reply_text('Сообщение должно содержать заголовок и содержание, разделенные новой строкой.')
        return

    news = News.save_news(title=title, content=content)
    update.message.reply_text(f'Новость сохранена с ID: {news.id}')

def main() -> None:
    # Создаем экземпляр Application и передаем ему токен вашего бота
    application = Application.builder().token("6654691259:AAHkgYkB5amPZlnwldEnD4S9-BOFDNcAAN4").build()

    # Регистрируем обработчик текстовых сообщений в группе
    application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUP, handle_group_message))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
