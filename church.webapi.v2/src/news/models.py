import uuid
from datetime import datetime
from create_app import db
from sqlalchemy import inspect
from sqlalchemy.orm import validates

class News(db.Model):
    """
    Модель данных для новостей.

    Attributes:
        news_id (UUID): Уникальный идентификатор новости.
        news_type_id (UUID): Уникальный идентификатор типа новости (связанный внешний ключ).
        news_type (Relationship): Связь с типом новости.
        news_number (Integer): Номер новости.
        news_image (Relationship): Связь с изображениями новости.
        news_title (Text): Заголовок новости.
        news_date (DateTime): Дата и время новости (по умолчанию, текущая дата и время).
        news_description (Text): Описание новости.

    """
    __tablename__ = "tbnews"
    news_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4, unique=True)
    news_type_id = db.Column(db.UUID, db.ForeignKey("news_type.id"))
    news_type = db.relationship("NewsType", backref=db.backref("news_type", lazy="dynamic"))
    news_number = db.Column(db.Integer)
    news_image = db.relationship("NewsImage", back_populates="tbnews")
    news_title = db.Column(db.Text)
    news_date = db.Column(db.DateTime, default=datetime.now)
    news_description = db.Column(db.Text)

class NewsImage(db.Model):
    """
    Модель данных для изображений новостей.

    Attributes:
        id (UUID): Уникальный идентификатор изображения.
        image_data (LargeBinary): Данные изображения.
        mimetype (Text): MIME-тип изображения.
        name (Text): Имя изображения.
        news_id_fk (UUID): Уникальный идентификатор связанной новости (связанный внешний ключ).
        tbnews (Relationship): Связь с новостью.

    """
    __tablename__ = "news_image"
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4, unique=True)
    image_data = db.Column(db.LargeBinary)
    mimetype = db.Column(db.Text)
    name = db.Column(db.Text)
    news_id_fk = db.Column(db.UUID, db.ForeignKey("tbnews.news_id"))
    tbnews = db.relationship("News", back_populates="news_image")

class NewsType(db.Model):
    """
    Модель данных для типов новостей.

    Attributes:
        id (UUID): Уникальный идентификатор типа новости.
        type_name (Text): Название типа новости.
        source (Text): Источник новостей.

    """
    __tablename__ = "news_type"
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4, unique=True)
    type_name = db.Column(db.Text)
    source = db.Column(db.Text)
