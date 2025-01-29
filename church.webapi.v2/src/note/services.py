import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Blueprint, request, jsonify
from .models import PaymentNote, PaymentNoteType, PaymentNoteName
from .serialize import PaymentNoteSchema, PaymentNoteTypeSchema, PaymentNoteNameSchema
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from create_app import db

payment_note_schema = PaymentNoteSchema()
payment_notes_schema = PaymentNoteSchema(many=True)
payment_note_type_schema = PaymentNoteTypeSchema(many=True)
payment_note_name_schema = PaymentNoteNameSchema(many=True)

def get_note_type():
    type = PaymentNoteType.query.all()
    result = payment_note_type_schema.dump(type, many=True)
    return jsonify(result), 200

def get_note_name():
    name = PaymentNoteName.query.all()
    result = payment_note_name_schema.dump(name, many=True)
    return jsonify(result), 200

def get_payment_notes():
    payment_notes = PaymentNote.query.all()
    result = payment_notes_schema.dump(payment_notes, many=True)
    return jsonify(result), 200

def get_payment_note(id):
    payment_note = PaymentNote.query.get(id)
    if not payment_note:
        return jsonify({"message": "Запись не найдена"}), 404
    result = payment_note_schema.dump(payment_note)
    return jsonify(result), 200


def send_message(author, to_name, phone_number):
    """
    Отправляет электронное письмо через SMTP сервер.

    При вызове функции ожидается POST-запрос с данными формы, включая 'mail', 'question' и 'subject_title'.
    Функция пытается отправить письмо на адрес, указанный в 'mail', с указанной темой 'subject_title' и текстом письма 'question'.
    В случае успешной отправки письма, возвращает HTTP-код 200 и сообщение "Сообщение успешно отправлено".
    Если произошла ошибка при отправке письма, возвращает JSON-ответ с сообщением об ошибке и HTTP-код 500.

    В случае отсутствия 'mail', 'question' или 'subject_title' в данных формы, возвращает JSON-ответ с сообщением об
    отсутствии обязательных полей и HTTP-код 400.

    :return: JSON-ответ с результатом операции и соответствующим HTTP-кодом.
    """
    to = 'spasskysobor.ru@mail.ru'
    body = f'Запрос на записку от {author}, для {to_name}\nТелефон {phone_number}'
    subject_title = 'Запрос на записку'
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

def create_payment_note():
    data = request.json
    try:
        payment_note_type = PaymentNoteType.query.get(data.get("tbpayment_note_type_id"))
        payment_note_name = PaymentNoteName.query.get(data.get("tbpayment_note_name_id"))

        if not payment_note_type or not payment_note_name:
            return jsonify({"message": "Неверные данные для связанных полей"}), 400

        new_payment_note = PaymentNote(
            tbpayment_note_type_id=data["tbpayment_note_type_id"],
            tbpayment_note_name_id=data["tbpayment_note_name_id"],
            author=data["author"],
            phone_number=data["phone_number"],
            to_name=data["to_name"]
        )
        
        db.session.add(new_payment_note)
        db.session.commit()
        result = payment_note_schema.dump(new_payment_note)
        send_message(author=data["author"], to_name=data["to_name"], phone_number=data["phone_number"])
      
                    
        return jsonify(result), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
 

def update_payment_note(payment_note_id):
    data = request.json
    try:
        payment_note = PaymentNote.query.get(payment_note_id)
        
        if not payment_note:
            return jsonify({"message": "Платежное примечание не найдено"}), 404

        payment_note_type = PaymentNoteType.query.get(data.get("tbpayment_note_type_id"))
        payment_note_name = PaymentNoteName.query.get(data.get("tbpayment_note_name_id"))

        if not payment_note_type or not payment_note_name:
            return jsonify({"message": "Неверные данные для связанных полей"}), 400

        payment_note.tbpayment_note_type_id = data.get("tbpayment_note_type_id", payment_note.tbpayment_note_type_id)
        payment_note.tbpayment_note_name_id = data.get("tbpayment_note_name_id", payment_note.tbpayment_note_name_id)
        payment_note.author = data.get("author", payment_note.author)
        payment_note.phone_number = data.get("phone_number", payment_note.phone_number)
        payment_note.to_name = data.get("to_name", payment_note.to_name)
        payment_note.at_work = data.get("at_work", payment_note.at_work)
        payment_note.finish = data.get("finish", payment_note.finish)
        
        db.session.commit()

        result = payment_note_schema.dump(payment_note)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400



payment_note_type_schema = PaymentNoteTypeSchema()
payment_note_name_schema = PaymentNoteNameSchema()

# PaymentNoteType Services
def create_payment_note_type():
    data = request.json
    try:
        new_note_type = PaymentNoteType(name=data["name"], cost=data["cost"])
        db.session.add(new_note_type)
        db.session.commit()
        result = payment_note_type_schema.dump(new_note_type)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def update_payment_note_type(note_type_id):
    data = request.json
    try:
        note_type = PaymentNoteType.query.get(note_type_id)
        if not note_type:
            return jsonify({"message": "Запись не найдена"}), 404
        note_type.name = data["name"]
        note_type.cost = data["cost"]
        db.session.commit()
        result = payment_note_type_schema.dump(note_type)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_payment_note_type(note_type_id):
    try:
        note_type = PaymentNoteType.query.get(note_type_id)
        if not note_type:
            return jsonify({"message": "Запись не найдена"}), 404
        db.session.delete(note_type)
        db.session.commit()
        return jsonify({"message": "Запись успешно удалена"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PaymentNoteName Services
def create_payment_note_name():
    data = request.json
    try:
        new_note_name = PaymentNoteName(name=data["name"], id_type=data["id_type"], cost=data['cost'])
        db.session.add(new_note_name)
        db.session.commit()
        result = payment_note_name_schema.dump(new_note_name)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def update_payment_note_name(note_name_id):
    data = request.json
    try:
        note_name = PaymentNoteName.query.get(note_name_id)
        if not note_name:
            return jsonify({"message": "Запись не найдена"}), 404
        note_name.name = data["name"]
        note_name.id_type = data["id_type"]
        note_name.cost =data['cost']
        db.session.commit()
        result = payment_note_name_schema.dump(note_name)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def delete_payment_note_name(note_name_id):
    try:
        note_name = PaymentNoteName.query.get(note_name_id)
        if not note_name:
            return jsonify({"message": "Запись не найдена"}), 404
        db.session.delete(note_name)
        db.session.commit()
        return jsonify({"message": "Запись успешно удалена"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
