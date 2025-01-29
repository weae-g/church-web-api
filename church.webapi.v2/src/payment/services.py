import decimal
import os
import hmac
import json
import hashlib
import threading
from flask import Flask, request, jsonify, Blueprint
from yookassa import Payment, Configuration
from .models import PaymentInfo
from create_app import db
from dotenv import load_dotenv
import uuid
import datetime
import logging
from telegram import Bot
from .email.mail import (send_payment_email_donation, 
                         send_payment_email_health, 
                         send_payment_email_rest, 
                         send_payment_about,
                         send_payment_email_candle,
                         send_payment_email_brick, 
                         send_payment_about_start,
                         send_payment_about_candle)

from brick.models import Brick
from candle.models import Candle, CandelIcon, CandlePrayer, CandleType
from note.serialize import PaymentInfoSchema
from candle.serialize import CandleTypeSchema
from donation.models import Donation
from note.models import PaymentNote, PaymentNoteType, PaymentNoteName

load_dotenv()

payment_bp = Blueprint("payment", __name__)

Configuration.account_id = os.getenv('YOOKASSA_SHOP_ID')
Configuration.secret_key = os.getenv('YOOKASSA_SECRET_KEY')


TOKEN = '6654691259:AAHkgYkB5amPZlnwldEnD4S9-BOFDNcAAN4'
GROUP_CHAT_ID = '-1002425134664'  
bot = Bot(token=TOKEN)

import asyncio

event_loop = asyncio.new_event_loop()
threading.Thread(target=event_loop.run_forever).start()

async def send_message_async(message):
    await bot.send_message(chat_id=GROUP_CHAT_ID, text=message, disable_web_page_preview=True)

def send_message(message):
    asyncio.run_coroutine_threadsafe(send_message_async(message), event_loop)


@payment_bp.route('/create_payment/brick', methods=['POST'])
def create_payment_brick():
    try:
        name = request.json.get('name')
        message = request.json.get('message')
        cost = request.json.get('cost')
        color = request.json.get('color')
        mail = request.json.get('mail')

        if not all([name, message, cost, color, mail]):
            return jsonify({'error': 'All fields are required'}), 400

        amount_value = float(cost)
        payment_idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": str(amount_value),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://spasskysobor.ru/thank_you"
            },
            "capture": True
        }, payment_idempotence_key)

        new_payment = PaymentInfo(
            payment_id=payment.id,
            amount=amount_value,
            currency='RUB',
            status=payment.status,
            user_email=mail,
            from_name=name,
            phone_number=None,
            note_cost=cost,
            donation=message,
            note_type="Кирпич",
            candle_type=None,
            candle_icon=None,
            candle_payer=color,
            day=None
        )
        db.session.add(new_payment)
        db.session.commit()

        

        payment_url = payment.confirmation.confirmation_url
        return jsonify({
            'payment_url': payment_url,
            'payment_id': payment.id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/create_payment', methods=['POST'])
def create_payment():
    try:
        amount = request.json.get('amount')
        description = request.json.get('description')
        user_email = request.json.get('user_email')
        from_name = request.json.get('from_name')
        user_name = request.json.get('user_name')
        phone_number = request.json.get('phone_number')
        note_cost = request.json.get('note_cost')
        note_name = request.json.get('note_name')
        note_type = request.json.get('note_type')
        donation = request.json.get('donation')
        payment_type = request.json.get('type')

        if not amount:
            return jsonify({'error': 'Amount is required'}), 400

        amount_value = float(amount)
        payment_idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": str(amount_value),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://spasskysobor.ru/thank_you"
            },
            "capture": True,
            "description": description
        }, payment_idempotence_key)

        new_payment = PaymentInfo(
            payment_id=payment.id,
            amount=amount_value,
            currency='RUB',
            status=payment.status,
            user_email=user_email,
            from_name=from_name,
            user_name=user_name,
            phone_number=phone_number,
            note_cost=note_cost,
            note_name=note_name,
            note_type=note_type,
            donation=donation,
            type=payment_type
        )
        db.session.add(new_payment)
        db.session.commit()

        payment_url = payment.confirmation.confirmation_url
        return jsonify({
            'payment_url': payment_url,
            'payment_id': payment.id
            }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/create_payment/trebi', methods=['POST'])
def create_payment_trebi():
    try:
        amount = request.json.get('amount')
        note_cost = request.json.get('amount')
        payment_note_type_id = request.json.get('payment_note_type_id')
        payment_note_name_id = request.json.get('payment_note_name_id')
        from_name = request.json.get('author')
        user_name = request.json.get('to_name')
        phone_number = request.json.get('phone_number')
        user_email = request.json.get('user_email')

        if not amount:
            return jsonify({'error': 'Amount is required'}), 400

        amount_value = float(amount)
        payment_idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": str(amount_value),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://spasskysobor.ru/thank_you"
            },
            "capture": True
        }, payment_idempotence_key)

        new_payment = PaymentInfo(
            payment_id=payment.id,
            amount=amount_value,
            currency='RUB',
            status=payment.status,
            user_email=user_email,
            from_name=from_name,
            user_name=user_name,
            phone_number=phone_number,
            note_cost=note_cost,
            note_name=payment_note_name_id,
            note_type=payment_note_type_id
        )
        db.session.add(new_payment)
        db.session.commit()

        print(new_payment.note_type)

        payment_url = payment.confirmation.confirmation_url
        return jsonify({
            'payment_url': payment_url,
            'payment_id': payment.id
            }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/create_payment/donation', methods=['POST'])
def create_payment_donation():
    try:
        donation_sum = request.json.get('donation_sum')
        note_cost = request.json.get('donation_sum')
        donation_name = request.json.get('donation_name')
        description = request.json.get('description')
        phone_number = request.json.get('phone_number')
        mail = request.json.get('mail')

        if not donation_sum:
            return jsonify({'error': 'Amount is required'}), 400

        amount_value = float(donation_sum)
        payment_idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": str(amount_value),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://spasskysobor.ru/thank_you"
            },
            "capture": True
        }, payment_idempotence_key)

        new_payment = PaymentInfo(
            payment_id=payment.id,
            amount=amount_value,
            currency='RUB',
            status=payment.status,
            user_email=mail,
            from_name=donation_name,
            phone_number=phone_number,
            note_cost=note_cost,
            donation=description,
            note_type="Пожертвования"
        )
        db.session.add(new_payment)
        db.session.commit()

        payment_url = payment.confirmation.confirmation_url

     

        return jsonify({
            'payment_url': payment_url,
            'payment_id': payment.id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/create_payment/candle', methods=['POST'])
def create_payment_candle():
    try:
        candle_type_id = request.json.get('candle_type_id')
        candle_icon_id = request.json.get('candle_icon_id')
        candle_prayer_id = request.json.get('candle_prayer_id')

        cost = request.json.get('cost')
        to_name = request.json.get('to_name')
        author = request.json.get('author')
        phone_number = request.json.get('phone_number')
        mail = request.json.get('mail')

        if not all([candle_type_id, candle_icon_id, candle_prayer_id, cost, to_name, author, phone_number, mail]):
            return jsonify({'error': 'All fields are required'}), 400

       

        if not all([candle_type_id, candle_icon_id, candle_prayer_id]):
            return jsonify({'error': 'Invalid candle_type_id, candle_icon_id or candle_prayer_id'}), 400

        amount_value = float(cost)
        payment_idempotence_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": str(amount_value),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://spasskysobor.ru/thank_you"
            },
            "capture": True
        }, payment_idempotence_key)

        new_payment = PaymentInfo(
            payment_id=payment.id,
            amount=amount_value,
            currency='RUB',
            status=payment.status,
            user_email=mail,
            from_name=author,
            phone_number=phone_number,
            note_cost=cost,
            user_name=to_name,
            donation='',
            note_type="Свечи",
            candle_type=candle_type_id,
            candle_icon=candle_icon_id,
            candle_payer=candle_prayer_id,
            day= datetime.datetime.now().date()
        )
        db.session.add(new_payment)
        db.session.commit()

      
        payment_url = payment.confirmation.confirmation_url
        return jsonify({
            'payment_url': payment_url,
            'payment_id': payment.id
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/send_payment_about/<int:payment_note_id>', methods=['POST'])
def send_payment_about_router(payment_note_id):
    try:   
        payment_note = PaymentNote.query.get(payment_note_id)
        payeer_note = PaymentInfo.query.get(payment_note.payment_id)
        update_payment_note(payment_note_id,at_work=True,finish=True)

        payment_note_schema = PaymentInfoSchema()    
        result = payment_note_schema.dump(payeer_note)
        user_name = result.get('from_name')
        cost = result.get('note_cost')
        user_email = result.get('user_email')
        note_name = result.get('note_name')
        send_payment_about(user_name, cost, user_email, note_name)



        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@payment_bp.route('/send_payment_about_candle/<int:payment_candle_id>', methods=['POST'])
def send_payment_about_candle_router(payment_candle_id):
    try:   
        payment_candle = Candle.query.get(payment_candle_id)
        payeer_candle = PaymentInfo.query.get(payment_candle.payment_id)
        
        candle_type_id = payment_candle.tbpayment_candel_type_id
        candle_type = CandleType.query.get(candle_type_id)
        
        payment_candle.finish = True
        db.session.commit()

        payment_note_schema = PaymentInfoSchema()    
        result = payment_note_schema.dump(payeer_candle)
        payment_candle_schema = CandleTypeSchema()
        result_candle_type = payment_candle_schema.dump(candle_type)
        user_name = result.get('from_name')
        cost = result_candle_type.get('name')
        user_email = result.get('user_email')
        note_name = result.get('note_name')
        send_payment_about_candle(user_name, cost, user_email, note_name)

        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@payment_bp.route('/send_payment_about_start/<int:payment_note_id>', methods=['POST'])
def send_payment_start_router(payment_note_id):
    try:   
        payment_note = PaymentNote.query.get(payment_note_id)
        payeer_note = PaymentInfo.query.get(payment_note.payment_id)
        update_payment_note(payment_note_id, at_work=True)

        payment_note_schema = PaymentInfoSchema()    
        result = payment_note_schema.dump(payeer_note)
        user_name = result.get('from_name')
        cost = result.get('note_cost')
        user_email = result.get('user_email')
        note_name = result.get('note_name')
        send_payment_about_start(user_name, cost, user_email, note_name)

        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def update_payment_note(payment_note_id, at_work=False, finish=False):
    try:
        payment_note = PaymentNote.query.get(payment_note_id)

        payment_note.at_work = at_work
        payment_note.finish = finish
        
        db.session.commit()

        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

def create_note(payment_note_type_id, payment_note_name_id,
                author, phone_number, to_name,payment_id):
    try:

        new_payment_note = PaymentNote(
            tbpayment_note_type_id=payment_note_type_id,
            tbpayment_note_name_id=payment_note_name_id,
            author=author,
            phone_number=phone_number,
            to_name=to_name,
            payment_id=payment_id
        )
        
        db.session.add(new_payment_note)
        db.session.commit()

        return jsonify({'status': 'ok'}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

import logging

logging.basicConfig(level=logging.DEBUG)

@payment_bp.route('/yookassa-webhook', methods=['POST'])
def yookassa_webhook():
    try:
        body = request.get_data(as_text=True)
        signature = request.headers.get('Authorization')
        secret_key = os.getenv('YOOKASSA_SECRET_KEY')

        event = request.json
        logging.info(f'Parsed JSON event: {event}')
        #print(event)

        if event['event'] == 'payment.succeeded':
            payment = event['object']
            payment_info = PaymentInfo.query.filter_by(payment_id=payment['id']).first()

            if payment_info and not payment_info.email_sent == True and payment_info.note_type == "Пожертвования":
                # Обновление статуса платежа
                process_successful_payment(payment)

                

               
                data = {
                    "donation_sum": payment_info.note_cost,
                    "donation_name": payment_info.from_name,
                    "description": payment_info.donation,
                    "phone_number": payment_info.phone_number,
                    "mail": payment_info.user_email 
                }

                new_donation = Donation(**data)
                db.session.add(new_donation)
                db.session.commit()             

                # Установка флага email_sent
                payment_info.email_sent = True
                db.session.commit()

                message = (
                    f"Новое пожертвование:\n"
                    f"Сумма: {payment_info.note_cost}\n"
                    f"Имя: {payment_info.from_name}\n"
                    f"Описание: {payment_info.donation}\n"
                    f"Телефон: {payment_info.phone_number}\n"
                    f"Email: {payment_info.user_email}"
                    )

                # Отправка сообщения в Telegram
                send_message(message)

                # Отправка email
                send_payment_email_donation(
                    payment_info.from_name,
                    payment_info.note_cost,
                    payment_info.user_email,
                    payment_info.phone_number,
                    payment_info.donation
                )
            elif payment_info and not payment_info.email_sent == True and payment_info.note_type == "1":
                # Обновление статуса платежа
                process_successful_payment(payment)

                payment_note_type = PaymentNoteType.query.filter_by(id=payment_info.note_type).first()
                payment_note_name = PaymentNoteName.query.filter_by(id=payment_info.note_name).first()           

                # Проверка на наличие нужных объектов
                if payment_note_type is None or payment_note_name is None:
                    raise ValueError("Не удалось найти тип или название платежа")

                

                message = (
                    f"Новый платеж:\n"
                    f"Тип: {payment_note_type.name}\n"
                    f"Сумма: {payment_info.note_cost}\n"
                    f"Имя: {payment_info.from_name}\n"
                    f"Телефон: {payment_info.phone_number}\n"
                    f"Email: {payment_info.user_email}\n"
                    f"Описание: {payment_note_name.name}\n"
                )

                # Отправка сообщения в Telegram
                send_message(message)

                # Установка флага email_sent
                payment_info.email_sent = True

                create_note(payment_info.note_type, payment_info.note_name,
                            payment_info.from_name, payment_info.phone_number,
                            payment_info.user_name, payment_info.id)
                db.session.commit()

                # Отправка email
                send_payment_email_health(
                    payment_info.phone_number,
                    payment_note_type.name,
                    payment_info.user_email,
                    payment_note_name.name,
                    payment_info.from_name,
                    payment_info.user_name,                  
                    payment_info.note_cost
                )
            elif payment_info and not payment_info.email_sent == True and payment_info.note_type == "2":
                # Обновление статуса платежа
                process_successful_payment(payment)

                payment_note_type = PaymentNoteType.query.filter_by(id=payment_info.note_type).first()
                payment_note_name = PaymentNoteName.query.filter_by(id=payment_info.note_name).first()           

                # Проверка на наличие нужных объектов
                if payment_note_type is None or payment_note_name is None:
                    raise ValueError("Не удалось найти тип или название платежа")

                

                message = (
                    f"Новый платеж:\n"
                    f"Тип: {payment_note_type.name}\n"
                    f"Сумма: {payment_info.note_cost}\n"
                    f"Имя: {payment_info.from_name}\n"
                    f"Телефон: {payment_info.phone_number}\n"
                    f"Email: {payment_info.user_email}\n"
                    f"Описание: {payment_note_name.name}\n"
                )

                # Отправка сообщения в Telegram
                send_message(message)

                # Установка флага email_sent
                payment_info.email_sent = True

                create_note(payment_info.note_type, payment_info.note_name,
                            payment_info.from_name, payment_info.phone_number,
                            payment_info.user_name, payment_info.id)
                db.session.commit()

                # Отправка email
                send_payment_email_health(
                    payment_info.phone_number,
                    payment_note_type.name,
                    payment_info.user_email,
                    payment_note_name.name,
                    payment_info.from_name,
                    payment_info.user_name,                  
                    payment_info.note_cost
                )
            elif payment_info and not payment_info.email_sent and payment_info.note_type == "Свечи":
                # Обновление статуса платежа
                process_successful_payment(payment)

                # Получаем из базы данных записи по ID                 
               
                candle_type = CandleType.query.filter_by(id=payment_info.candle_type).first()
                candle_icon = CandelIcon.query.filter_by(id=payment_info.candle_icon).first()
                candle_prayer = CandlePrayer.query.filter_by(id=payment_info.candle_payer).first()

                
                

                
                new_candle = Candle(
                    tbpayment_candel_type_id=candle_type.id,
                    tbpayment_candel_icon=candle_icon.id,
                    tbpayment_candel_prayer=candle_prayer.id,
                    cost=decimal.Decimal(payment_info.note_cost),
                    day=datetime.datetime.now(),
                    to_name=payment_info.user_name,
                    author=payment_info.from_name,
                    phone_number=payment_info.phone_number,
                    payment_id = payment_info.id
                )
                message = (
                    f"Новая свеча:\n"
                    f"Тип: {candle_type.name}\n"
                    f"Иконка: {candle_icon.name}\n"
                    f"Молитва: {candle_prayer.name}\n"
                    f"Сумма: {payment_info.note_cost}\n"
                    f"Имя: {payment_info.from_name}\n"
                    f"Телефон: {payment_info.phone_number}\n"
                    f"Email: {payment_info.user_email}\n"
                )

                # Отправка сообщения в Telegram
                send_message(message)
                payment_info.email_sent = True


                db.session.add(new_candle)
                db.session.commit()

                # Отправка email
                send_payment_email_candle(
                    payment_info.from_name,
                    payment_info.amount,
                    payment_info.user_email,
                    payment_info.phone_number,
                    candle_type.name,
                    candle_icon.name,
                    candle_prayer.name
                )
            elif payment_info and not payment_info.email_sent and payment_info.note_type == "Кирпич":
                # Обновление статуса платежа
                process_successful_payment(payment)            

                   

                new_brick = Brick(
                    name=payment_info.from_name,
                    message=payment_info.donation,
                    cost=payment_info.note_cost,
                    color=payment_info.candle_payer,
                    mail=payment_info.user_email
                )

                message = (
                    f"Новый кирпич:\n"
                    f"Имя: {payment_info.from_name}\n"
                    f"Сообщение: {payment_info.donation}\n"
                    f"Сумма: {payment_info.note_cost}\n"
                    f"Цвет: {payment_info.candle_payer}\n"
                    f"Email: {payment_info.user_email}\n"
                )

                # Отправка сообщения в Telegram
                send_message(message)

                payment_info.email_sent = True
                db.session.add(new_brick)
                db.session.commit()

                # Отправка email
                send_payment_email_brick(
                    user_name=payment_info.from_name,
                    message=payment_info.donation,
                    cost=payment_info.amount,
                    color=payment_info.candle_payer,
                    user_email=payment_info.user_email
                )

        elif event['event'] == 'payment.waiting_for_capture':
            payment = event['object']
            update_payment_status(payment, 'waiting_for_capture')

        elif event['event'] == 'payment.canceled':
            payment = event['object']
            update_payment_status(payment, 'canceled')

        elif event['event'] == 'refund.succeeded':
            payment = event['object']
            update_payment_status(payment, 'refund_succeeded')

        description = payment.get('description', 'No description provided')

        return jsonify({'status': 'ok', 'description': description}), 200

    except Exception as e:
        logging.error(f'Error occurred: {str(e)}', exc_info=True) 
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/payments', methods=['GET'])
def get_all_payments():
    try:
        payments = PaymentInfo.query.all()
        payment_list = [
            {
                'payment_id': payment.payment_id,
                'amount': payment.amount,
                'currency': payment.currency,
                'status': payment.status
            } for payment in payments
        ]
        return jsonify(payment_list), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

@payment_bp.route('/payment_status/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    try:
        payment = PaymentInfo.query.filter_by(payment_id=payment_id).first()
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        return jsonify({'status': payment.status}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def verify_signature(body, signature, secret_key):
    if signature is None:
        return False
    hash_string = hmac.new(secret_key.encode('utf-8'), body.encode('utf-8'), hashlib.sha256).hexdigest()

    return hmac.compare_digest(f'Bearer {hash_string}', signature)

def process_successful_payment(payment):
    payment_info = PaymentInfo.query.filter_by(payment_id=payment['id']).first()
    if payment_info:
        payment_info.status = 'succeeded'
        db.session.commit()


def update_payment_status(payment, status):
    payment_info = PaymentInfo.query.filter_by(payment_id=payment['id']).first()
    if payment_info:
        payment_info.status = status
        db.session.commit()
