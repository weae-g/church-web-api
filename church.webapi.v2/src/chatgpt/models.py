from create_app import db
from datetime import datetime
import uuid

class TbQuestios(db.Model):
    """
    Модель данных для хранения вопросов и ответов.

    Attributes:
        id (UUID): Уникальный идентификатор записи (только для чтения).
        question (Text): Вопрос.
        answer (Text): Ответ на вопрос.
        date (DateTime): Дата и время создания записи (по умолчанию, текущая дата и время).

    """
    __tablename__ = "tbquestios_ai"
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4(), unique=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.now)
