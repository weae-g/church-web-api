from marshmallow import Schema, fields, validate, ValidationError, pre_load

class ChatBotSchema(Schema):
    """
    Схема для сериализации и десериализации данных модели TbQuestios.

    Fields:
        id (UUID): Уникальный идентификатор записи (только для чтения).
        question (Str): Вопрос (обязательное поле).
        answer (Str): Ответ на вопрос (обязательное поле).
        date (DateTime): Дата и время создания записи.

    """
    id = fields.UUID(dump_only=True)
    question = fields.Str(required=True)
    answer = fields.Str(required=True)
    date = fields.DateTime()
