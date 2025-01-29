"""
Модуль, содержащий определения SQLAlchemy-моделей для работы с данными сотрудников и их ролями и изображениями.

Классы:
    - Employee: Модель сотрудника, хранит основные данные о сотруднике, такие как имя, электронная почта, телефон и описание.
    - EmployeeRole: Модель роли сотрудника, связана с сотрудниками и хранит информацию о ролях.
    - EmployeeImage: Модель изображения сотрудника, связана с сотрудниками и хранит пути к изображениям.

Эти классы предназначены для работы с базой данных и обеспечивают операции создания, обновления и удаления записей.
"""
from sqlalchemy.orm import relationship
import uuid

from create_app import db

class Employee(db.Model):
    __tablename__ = "tbemployee"
    employee_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    employee_name = db.Column(db.Text) 
    employee_email = db.Column(db.Text)
    employee_phone = db.Column(db.Text)
    employee_description_about = db.Column(db.Text)
    employee_date = db.Column(db.DateTime)  
   
    employee_role = relationship(
        "EmployeeRole",  backref=db.backref("employees")
    )
    employee_image = relationship(
        "EmployeeImage", back_populates="employee"
    )


class EmployeeRole(db.Model):
    __tablename__ = "employee_role"
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    name = db.Column(db.Text)
    employee_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tbemployee.employee_id"))
    


class EmployeeImage(db.Model):
    __tablename__ = "employee_image"
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    image = db.Column(db.LargeBinary)
    employee_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey("tbemployee.employee_id"), unique=True)  # Добавляем ограничение уникальности
    employee = relationship("Employee", back_populates="employee_image")

 
