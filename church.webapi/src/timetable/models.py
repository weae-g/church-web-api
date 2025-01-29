import sys
from sqlalchemy import inspect
from datetime import datetime

from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
import uuid
from create_app import db



class TimeTable(db.Model):
    """
    Модель данных для расписания.

    Attributes:
        tbtimetable_id (UUID): Уникальный идентификатор расписания.
        tbtimetable_date (DateTime): Дата расписания.
        tbtimetable_duty (Text): Задачи или дежурства в расписании.
        tbtimetable_name (Text): Название расписания.
        timetable_time (Time): Время расписания.

    Methods:
        create(cls, data): Создает новую запись расписания на основе переданных данных.
        delete(self): Удаляет текущую запись расписания.
        update(self, data): Обновляет текущую запись расписания на основе переданных данных.

    """
    __tablename__ = "tbtimetable"
    tbtimetable_id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    tbtimetable_date = db.Column(db.DateTime)
    tbtimetable_duty = db.Column(db.Text)
    tbtimetable_name = db.Column(db.Text)
    timetable_time = db.Column(db.Time)
    employees = relationship('TimeTableEmployee', back_populates='timetable')

    @classmethod
    def create(cls, data):
        """
        Создает новую запись расписания на основе переданных данных.

        Args:
            cls: Класс TimeTable.
            data (dict): Словарь данных для создания новой записи.

        Returns:
            TimeTable: Новая запись расписания.

        """
        new_timetable = cls(**data)
        db.session.add(new_timetable)
        db.session.commit()
        return new_timetable

    def delete(self):
        """
        Удаляет текущую запись расписания.

        """
        db.session.delete(self)
        db.session.commit()
    
    def update(self, data):
        """
        Обновляет текущую запись расписания на основе переданных данных.

        Args:
            data (dict): Словарь данных для обновления записи.

        """    
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

class TimeTableEmployee(db.Model):
    """
    Модель данных для записей о сотрудниках в расписании.

    Attributes:
        id (UUID): Уникальный идентификатор записи о сотруднике.
        name (Text): Имя сотрудника.
        time_table_id (UUID): Уникальный идентификатор связанного расписания.

    Methods:
        create(cls, data): Создает новую запись о сотруднике на основе переданных данных.
        delete(self): Удаляет текущую запись о сотруднике.
        update(self, data): Обновляет текущую запись о сотруднике на основе переданных данных.

    """
    __tablename__ = "timetable_employee"
    id = db.Column(db.UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text)
    time_table_id = db.Column(db.UUID, db.ForeignKey('tbtimetable.tbtimetable_id'))
    timetable = relationship('TimeTable', back_populates='employees')
    
    @classmethod
    def create(cls, data):       
        """
        Создает новую запись о сотруднике на основе переданных данных.

        Args:
            cls: Класс TimeTableEmployee.
            data (dict): Словарь данных для создания новой записи.

        Returns:
            TimeTableEmployee: Новая запись о сотруднике.

        """
        new_employee = cls(**data)
        db.session.add(new_employee)
        db.session.commit()
        return new_employee

    def delete(self):
        """
        Удаляет текущую запись о сотруднике.

        """
        db.session.delete(self)
        db.session.commit()
        
    def update(self, data):        
        """
        Обновляет текущую запись о сотруднике на основе переданных данных.

        Args:
            data (dict): Словарь данных для обновления записи.

        """
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()

