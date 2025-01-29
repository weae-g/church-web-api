import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from create_app import db
from .models import Brick
from .serialize import BrickSchema, BrickSchemaCreate
from flask import request, jsonify

brickSchemaCreate_schema = BrickSchemaCreate()
brickSchema_schema = BrickSchema()
brickSchema_schemas = BrickSchema(many=True)

def get_all():
    try:
        brick_type = db.session.query(Brick).all()
        return brickSchema_schemas.dump(brick_type), 201
    except Exception as e:
        return jsonify({"error" : str(e)})



def create_brick():
    try:
        # Десериализация данных из запроса
        brick_data = request.get_json()
        new_brick = brickSchemaCreate_schema.load(brick_data)
        
        # Создание нового объекта Brick
        brick = Brick(**new_brick)
        
        # Добавление нового объекта в сессию и сохранение в базе данных
        db.session.add(brick)
        db.session.commit()
        
        # Сериализация объекта Brick обратно в JSON
        result = brickSchema_schema.dump(brick)
        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

def delete_brick(id):
    try:
        # Поиск объекта Brick по ID
        brick = db.session.query(Brick).get(id)
        
        if brick is None:
            return jsonify({"error": "Плитка не найдена"}), 404
        
        # Удаление объекта из сессии и базы данных
        db.session.delete(brick)
        db.session.commit()
        
        return jsonify({"message": "Плитка успешно удалена"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400