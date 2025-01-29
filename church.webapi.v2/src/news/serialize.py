from marshmallow import Schema, fields, ValidationError
import base64

class NewsImageSchema(Schema):
    """
    Схема для сериализации и десериализации данных модели NewsImage.

    Fields:
        id (UUID): Уникальный идентификатор изображения (только для чтения).
        mimetype (Str): MIME-тип изображения (обязательное поле).
        name (Str): Имя изображения (обязательное поле).

    Methods:
        load_image_data(self, obj, data): Метод для десериализации base64 данных в image_data.
        dump_image_data(self, obj): Метод для сериализации image_data в base64.

    """
    id = fields.UUID(dump_only=True)
    mimetype = fields.Str(required=True)
    name = fields.Str(required=True)
    
    def load_image_data(self, obj, data):
        """
        Метод для десериализации base64 данных в image_data.

        Args:
            obj: Объект NewsImage.
            data (dict): Данные для десериализации.

        Returns:
            obj: Объект NewsImage с обновленными данными.

        Raises:
            ValueError: Если произошла ошибка декодирования изображения.

        """
        if 'image_data' in data:
            try:
                image_data = base64.b64decode(data['image_data'])
                obj.image_data = image_data
            except Exception as e:
                raise ValueError(f"Ошибка декодирования изображения: {e}")
        return obj

    def dump_image_data(self, obj):
        """
        Метод для сериализации image_data в base64.

        Args:
            obj: Объект NewsImage.

        Returns:
            dict: Сериализованные данные с изображением в формате base64.

        """
        if obj.image_data:
            return {'image_data': base64.b64encode(obj.image_data).decode('utf-8')}
        return {}

class NewsTypeSchema(Schema):
    """
    Схема для сериализации и десериализации данных модели NewsType.

    Fields:
        id (UUID): Уникальный идентификатор типа новости (только для чтения).
        type_name (Str): Название типа новости.
        source (Str): Источник новостей.

    """
    id = fields.UUID(dump_only=True)
    type_name = fields.Str()
    source = fields.Str()

class NewsSchema(Schema):
    """
    Схема для сериализации и десериализации данных модели News.

    Fields:
        news_id (UUID): Уникальный идентификатор новости (только для чтения).
        news_image (Nested): Сериализованные данные изображений новости (множественное поле).
        news_number (Integer): Номер новости.
        news_type (Nested): Сериализованные данные типа новости.

    """
    news_id = fields.UUID(dump_only=True)
    news_image = fields.Nested(NewsImageSchema, many=True)
    news_number = fields.Integer()
    news_type = fields.Nested(NewsTypeSchema)
    news_title = fields.Str()
    news_date = fields.Str()
    news_description = fields.Str()
