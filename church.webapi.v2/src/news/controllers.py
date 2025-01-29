from flask import request, jsonify, Blueprint, Response, send_file
from flask_cors import CORS, cross_origin
from flask_login import  login_required
from .services import (
    get_news_at_russ,
    get_image_collection,    
    get_all_news_count,
    get_last,
    get_list_news,    
    get_news_by_type,
    get_one_news,   
    delete_news_by_id,
    delete_news_image_by_id,
    update_news_image,   
    update_news,    
    create_news,
    create_news_image,
    search_news_by_date,   
    search_news_by_name
)

news_bp = Blueprint("news", __name__)

@news_bp.route('/get_image/<uuid:image_id>' , methods=["GET"])
#@cross_origin(allow_headers=["Content-Type"], allow_methods=["GET"])
def get_image(image_id):
    """
    Получает изображение по его уникальному идентификатору (UUID).

    :param image_id: Уникальный идентификатор изображения (UUID).
    :type image_id: str

    :return: Изображение в виде бинарных данных и соответствующего MIME-типа, или сообщение об ошибке.
    :rtype: Response
    """
    try:
        return get_image_collection(image_id=image_id)
    except Exception as e:
        return jsonify({"Ошибка" : str(e)}), 500

@news_bp.route('/news/search_by_date', methods=["GET"])
def search_news_by_date_route():
    try:
        return search_news_by_date()
    except Exception as e:
        return jsonify({"error" : str(e)})

@news_bp.route('/news/search_by_name', methods=["GET"])
def search_news_by_name_route():
    try:
        return search_news_by_name()
    except Exception as e:
        return jsonify({"error" : str(e)})

@news_bp.route('/news/russ', methods=["GET"])
def get_news_russ():
    return get_news_at_russ(), 201

@news_bp.route("/news/<uuid>", methods=["GET"])
def one_news(uuid):
    """
    Получает одну новость по её уникальному идентификатору (UUID).

    :param uuid: Уникальный идентификатор новости (UUID).
    :type uuid: str

    :return: Данные одной новости или сообщение об ошибке, если новость не найдена.
    :rtype: Response
    """
    try:
        return get_one_news(uuid)    
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500

@news_bp.route("/news", methods=["GET"])
def list_news():
    """
    Получает список всех новостей.

    :return: Список всех новостей или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:
        return get_list_news()
    except Exception as e:
        return jsonify({"Ошибка" ,str(e)}), 500
    
@news_bp.route("/news/last", methods=["GET"])
def list_last(count = 50):
    try:
        return get_last(count)
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    
@news_bp.route("/news/count", methods=["GET"])
def list_news_count():
    """
    Получает общее количество новостей.

    :return: Общее количество новостей или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:
        return get_all_news_count()
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500

@news_bp.route("/news/type", methods=["GET"])
def get_news_by_type_and_count():
    """
    Получает новости определенного типа с учетом пагинации.

    :return: Список новостей заданного типа и информацию о пагинации или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:       
        return get_news_by_type()
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500
  
@news_bp.route("/news", methods=["POST"])
@login_required
def create_new_news():
    """
    Создает новую новость и сохраняет ее в базе данных.

    :return: Сообщение о успешном создании новости или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:
        return create_news()
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500

@news_bp.route("/news/image", methods=["POST"])
@login_required
def create_new_news_image():
    """
    Создает новую новость и сохраняет ее в базе данных.

    :return: Сообщение о успешном создании новости или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:
        return create_news_image()
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500

@news_bp.route('/news/images/<uuid:image_id>', methods=['PUT'])
@login_required
def put_update_image(image_id):
    """
    Обновляет данные изображения по его идентификатору.

    :param image_id: Идентификатор изображения.
    :type image_id: UUID

    :return: Сообщение о успешном обновлении изображения или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:               
        result, status_code = update_news_image(image_id)
        return result, status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@news_bp.route("/news/<uuid:news_id>", methods=["PUT"])
@login_required
def put_update_news(news_id):
    """
    Обновляет данные новости по её идентификатору.

    :param news_id: Идентификатор новости.
    :type news_id: UUID

    :return: Сообщение о успешном обновлении новости или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:
        return update_news(news_id)    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@news_bp.route("/news/<uuid>", methods=["DELETE"])
@login_required
def delete_news(uuid):
    """
    Удаляет новость по её идентификатору.

    :param uuid: Идентификатор новости.
    :type uuid: UUID

    :return: Сообщение о успешном удалении новости или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:
        return delete_news_by_id(str(uuid))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@news_bp.route("/news/image/<uuid>", methods=["DELETE"])
@login_required
def delete_news_image(uuid):
    """
    Удаляет новость по её идентификатору.

    :param uuid: Идентификатор новости.
    :type uuid: UUID

    :return: Сообщение о успешном удалении новости или сообщение об ошибке, если что-то пошло не так.
    :rtype: Response
    """
    try:
        return delete_news_image_by_id(str(uuid))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

