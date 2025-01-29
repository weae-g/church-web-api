import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from create_app import db
from .models import Candle, CandelIcon, CandlePrayer, CandleType
from .serialize import CandleSchema, CandelIconSchema, CandlePrayerSchema, CandleTypeSchema
from flask import request, jsonify

candle_schema = CandleSchema()
candles_schema = CandleSchema(many=True)
candles_icon_schema = CandelIconSchema(many=True)
candles_prayer_schema = CandlePrayerSchema(many=True)
candles_type_schema = CandleTypeSchema(many=True)

def get_type():
    try:
        candle_type = db.session.query(CandleType).all()
        return candles_type_schema.dump(candle_type), 201
    except Exception as e:
        return jsonify({"error" : str(e)})

def get_icon():
    try:
        candle_icon = db.session.query(CandelIcon).all()
        return candles_icon_schema.dump(candle_icon), 201
    except Exception as e:
        return jsonify({"error" : str(e)})

def get_prayer():
    try:
        candle_prayer = db.session.query(CandlePrayer).all()
        return candles_prayer_schema.dump(candle_prayer), 201
    except Exception as e:
        return jsonify({"error" : str(e)})

def get_candle(candle_id):
    candle = db.session.query(Candle).get(candle_id)
    if candle:
        return candle_schema.dump(candle), 200
    return jsonify({"message": "Свеча отсутсвуют"}), 404

def send_message(author, to_name, phone_number):    
    to = 'spasskysobor.ru@mail.ru'
    body = f'Запрос на свечку от {author}, для {to_name}\nТелефон {phone_number}'    
    subject_title = 'Запрос на свечку'
    if not (to and body and subject_title):
        return jsonify({"error": "Отсутствуют обязательные поля"}), 400
    
    smtp_server = 'smtp.mail.ru'  
    smtp_port = 587  
    smtp_username = os.getenv("EMAIL_DATA_LOGIN")  
    smtp_password = os.getenv("EMAIL_DATA_PSWD")      
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_username, smtp_password)
        
        msg = MIMEMultipart()
        msg['From'] = 'spasskysobor.ru@mail.ru'
        msg['To'] = to
        msg['Subject'] = subject_title 
        msg.attach(MIMEText(body, 'plain'))
        server.sendmail('spasskysobor.ru@mail.ru', to, msg.as_string())
        
        print('Письмо успешно отправлено')
        return "Сообщение успешно отправлено", 200
    except smtplib.SMTPDataError as e:
        print(f'Отказ принятия письма: {str(e)}')
        return jsonify({"error": "Произошла ошибка при отправке письма"}), 500
    except Exception as e:
        print(f'Ошибка при отправке письма: {str(e)}')
        return jsonify({"error": "Произошла ошибка при отправке письма"}), 500

def create_candle():
    try:
        data = request.get_json()
        new_candle = Candle(**data)         
        db.session.add(new_candle)
        db.session.commit()
        send_message(author=data["author"], to_name=data["to_name"], phone_number=data["phone_number"])
        return candle_schema.dump(new_candle), 201
    except Exception as e:
        return jsonify({"message": "Неверный ввод", "error": str(e)}), 400


def get_candle_all():
    candle = db.session.query(Candle).all()
    if candle:
        return candles_schema.dump(candle), 200
    return jsonify({"message": "Свечи отсутсвуют"}), 404

# new
def create_candle_prayer():
    try:
        data = request.get_json()
        new_prayer = CandlePrayer(**data)
        db.session.add(new_prayer)
        db.session.commit()
        return jsonify({"message": "CandlePrayer создана", "data": CandlePrayerSchema().dump(new_prayer)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def update_candle_prayer(prayer_id):
    try:
        data = request.get_json()
        prayer = db.session.query(CandlePrayer).get(prayer_id)
        if not prayer:
            return jsonify({"message": "CandlePrayer не найдена"}), 404

        for key, value in data.items():
            setattr(prayer, key, value)

        db.session.commit()
        return jsonify({"message": "CandlePrayer обновлена", "data": CandlePrayerSchema().dump(prayer)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_candle_prayer(prayer_id):
    try:
        prayer = db.session.query(CandlePrayer).get(prayer_id)
        if not prayer:
            return jsonify({"message": "CandlePrayer не найдена"}), 404

        db.session.delete(prayer)
        db.session.commit()
        return jsonify({"message": "CandlePrayer удалена"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_candle_icon():
    try:
        data = request.get_json()
        new_icon = CandelIcon(**data)
        db.session.add(new_icon)
        db.session.commit()
        return jsonify({"message": "CandelIcon создана", "data": CandelIconSchema().dump(new_icon)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def update_candle_icon(icon_id):
    try:
        data = request.get_json()
        icon = db.session.query(CandelIcon).get(icon_id)
        if not icon:
            return jsonify({"message": "CandelIcon не найдена"}), 404

        for key, value in data.items():
            setattr(icon, key, value)

        db.session.commit()
        return jsonify({"message": "CandelIcon обновлена", "data": CandelIconSchema().dump(icon)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_candle_icon(icon_id):
    try:
        icon = db.session.query(CandelIcon).get(icon_id)
        if not icon:
            return jsonify({"message": "CandelIcon не найдена"}), 404

        db.session.delete(icon)
        db.session.commit()
        return jsonify({"message": "CandelIcon удалена"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
