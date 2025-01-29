import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_DATA_PSWD, EMAIL_DATA_LOGIN
from flask import request, jsonify, Blueprint


smtp_bp = Blueprint("smtp", __name__)


@smtp_bp.route("/smtp", methods=["POST"])
def send_message():
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
    to = request.form.get("mail", 'spasskysobor.ru@mail.ru')
    body = request.form.get("question")
    subject_title = request.form.get("subject_title")
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

