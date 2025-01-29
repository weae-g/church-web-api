from marshmallow import Schema, fields, ValidationError, pre_load
from flask import url_for
import base64


class GalleryTypeShema(Schema):
    """
    Схема для сериализации и десериализации данных типов галереи.

    Attributes:
        id (UUID): Идентификатор типа галереи (только для чтения).
        name (str): Наименование типа галереи.

    """

    id = fields.UUID(dump_only=True)
    name = fields.Str()

class AlbumSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    description = fields.Str()


class GallerySchema(Schema):
    """
    Схема для сериализации и десериализации данных галереи.
    """

    tbgallery_id = fields.UUID(dump_only=True)
    image_title = fields.Str()
    image_number = fields.Int()
    date = fields.DateTime()
    
    album_info = fields.Nested(AlbumSchema, attribute="album")
    
    gallery_type = fields.Nested(GalleryTypeShema)
    
    image = fields.Method("get_image_url")


    def get_image_url(self, gallery):
        if gallery.tbgallery_id:
            return url_for('gallery.get_gallery_image', tbgallery_id=gallery.tbgallery_id, _external=True)
        return None


class GallerySchemaOnse(Schema):
    """
    Схема для сериализации и десериализации данных галереи.
    """

    tbgallery_id = fields.UUID(dump_only=True)
    image_title = fields.Str()
    image_number = fields.Int()
    date = fields.DateTime()
    
    image = fields.Method("get_image_url")


    def get_image_url(self, gallery):
        if gallery.tbgallery_id:
            return url_for('gallery.get_gallery_image', tbgallery_id=gallery.tbgallery_id, _external=True)
        return None
