from flask import request, Blueprint, jsonify
from .models import TbQuestios
from .serialize import ChatBotSchema
from sqlalchemy import desc
import openai
from flask_login import login_required
from create_app import db

ChatBotSchemas = ChatBotSchema(many=True)

bot_bp = Blueprint("bot", __name__)


def send_to_base(question, answer):
    """
    Сохраняет вопрос и ответ в базу данных.

    Args:
        question (str): Вопрос, который нужно сохранить.
        answer (str): Ответ на вопрос, который нужно сохранить.

    Returns:
        bool: True, если сохранение прошло успешно, иначе False.

    """
    try:
        db.session.add(
            TbQuestios(
                question = question,
                answer = answer
            )
        )
        db.session.commit()
        return True
    except Exception as e:
        return False

@bot_bp.route("/bot/message/history", methods=["GET"])
#@login_required
def get_messages():
    """
    Получить историю сообщений бота.

    Функция выполняет запрос к базе данных для получения истории сообщений бота. Затем сериализует данные
    с использованием схемы ChatBotSchemas и возвращает их в формате JSON.

    Returns:
        jsonify(response): JSON-ответ с историей сообщений бота и кодом состояния 200 (OK).

    """
    try:
        items = TbQuestios.query.order_by(desc(TbQuestios.date)).all()

        response = ChatBotSchemas.dump(items)
        return jsonify(response), 200
    except Exception as e:
        return "Ошибка новостей" , 500

@bot_bp.route("/bot", methods=["POST"])
def output_message():
    """
    Отправить вопрос боту и получить ответ.

    Функция отправляет вопрос боту с использованием OpenAI GPT-3 и получает ответ. Затем сохраняет вопрос и ответ
    в базу данных. Если сохранение прошло успешно, возвращает JSON-ответ с вопросом и ответом и кодом состояния 201 (Created).
    В противном случае возвращает JSON-ответ с вопросом и ответом и кодом состояния 202 (Accepted).

    Returns:
        dict: JSON-ответ с вопросом и ответом бота.

    """
    try:
        openai.api_key = "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"

        model_engine = "gpt-3.5-turbo"

        completion = openai.ChatCompletion.create(
            model=model_engine,
            messages=[
                {"role": "system", "content": "Ты священник русской православной церкви"},
                {"role": "user", "content": request.form["question"]},
            ],
            max_tokens=1024,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        if(send_to_base(request.form["question"], completion.choices[0].message.content)):
            return {"question" : request.form["question"], "answer": completion.choices[0].message.content}, 201
        else:
            return {"question" : request.form["question"], "answer": completion.choices[0].message.content}, 202
    except openai.InvalidRequestError as e:
        pass
    except openai.OpenAIError as e:
        pass
    except Exception as e:
        pass
   
