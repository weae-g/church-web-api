import uuid
import datetime
from create_app import db
from sqlalchemy.orm import relationship

class Gallery(db.Model):
    __tablename__ = "tbgallery"
    tbgallery_id = db.Column(
        db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    image = db.Column(db.LargeBinary)
    gallery_type_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("gallery_type.id"))
    image_number = db.Column(db.Integer)
    gallery_type = relationship(
        "GalleryType", backref=db.backref("gallery", lazy="dynamic")
    )

class GalleryType(db.Model):
    """
    Модель данных для типов галереи.

    Attributes:
        id (UUID): Идентификатор типа галереи (первичный ключ).
        name (Text): Название типа галереи.
        source (Text): Источник типа галереи.

    """
    __tablename__ = "gallery_type"
    id = db.Column(
        db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    name = db.Column(db.Text)
    source = db.Column(db.Text)
