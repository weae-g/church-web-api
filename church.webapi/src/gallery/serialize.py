from marshmallow import Schema, fields, ValidationError, pre_load


class GalleryTypeShema(Schema):
    """
    Схема для сериализации и десериализации данных типов галереи.

    Attributes:
        id (UUID): Идентификатор типа галереи (только для чтения).
        name (str): Наименование типа галереи.

    """

    id = fields.UUID(dump_only=True)
    name = fields.Str()


class GallerySchema(Schema):
    """
    Схема для сериализации и десериализации данных галереи.

    Attributes:
        tbgallery_id (UUID): Идентификатор записи галереи (только для чтения).
        image_path (str): Путь к изображению.
        image_title (str): Название изображения.
        date (DateTime): Дата создания записи.
        gallery_type (Nested): Вложенная схема для типа галереи.

    """

    tbgallery_id = fields.UUID(dump_only=True)
    image = fields.Str()
    image_title = fields.Str()
    image_number = fields.Int()
    date = fields.DateTime()
    gallery_type = fields.Nested(GalleryTypeShema)
