from marshmallow import Schema, fields, ValidationError

class TimeTableSchema(Schema):
    """
    Схема для сериализации и десериализации данных модели TimeTable.

    Fields:
        tbtimetable_id (UUID): Уникальный идентификатор расписания (только для чтения).
        tbtimetable_time (DateTime): Дата и время расписания.
        tbtimetable_duty (Str): Задачи или дежурства в расписании.
        tbtimetable_name (Str): Название расписания.
        timetable_day (Str): День недели расписания.

    """
    tbtimetable_id = fields.UUID(dump_only=True)
    tbtimetable_time = fields.DateTime()
    tbtimetable_duty = fields.Str()
    tbtimetable_name = fields.Str()
    timetable_day = fields.Str()

class TimeTableEmployeeSchema(Schema):
    """
    Схема для сериализации и десериализации данных модели TimeTableEmployee.

    Fields:
        id (UUID): Уникальный идентификатор записи о сотруднике (только для чтения).
        name (Str): Имя сотрудника.
        time_table_id (Str): Уникальный идентификатор связанного расписания.

    """
    id = fields.UUID(dump_only=True)
    name = fields.Str()
    time_table_id = fields.Str()
