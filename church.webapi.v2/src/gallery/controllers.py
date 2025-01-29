from flask import request, jsonify, Blueprint
from flask_login import login_required
from .services import (
    get_gallery_data,
    get_gallery_image,
    create_gallery_info,
    update_gallery_info,
    delete_gallery_info,
    create_album, 
    get_album,
    get_all_albums,
    update_album,
    delete_album,
    get_gallery_data_by,
    delete_album,
    get_random_photos

)

gallery_bp = Blueprint("gallery", __name__)

@gallery_bp.route("/random_photos", methods=['GET'])
def get_random_photos_router():
    return get_random_photos()

# Роут для создания нового альбома
@gallery_bp.route('/album', methods=['POST'])
def create_new_album():
    return create_album()

@gallery_bp.route('/album/<uuid:album_id>', methods=['DELETE'])
@login_required
def delete_album_router(album_id):    
    return delete_album(album_id)

# Роут для получения всех альбомов
@gallery_bp.route('/album', methods=['GET'])
def get_all_album():
    return get_all_albums()

# Роут для получения конкретного альбома по его id
@gallery_bp.route('/album/<uuid:album_id>', methods=['GET'])
def get_specific_album(album_id):
    return get_album(album_id)

# Роут для обновления альбома по его id
@gallery_bp.route('/album/<uuid:album_id>', methods=['PUT'])
@login_required
def update_specific_album(album_id):
    return update_album(album_id)

# Роут для удаления альбома по его id
@gallery_bp.route('/album/<uuid:album_id>', methods=['DELETE'])
@login_required
def delete_specific_album(album_id):
    return delete_album(album_id)

@gallery_bp.route('/gallery/image/<tbgallery_id>', methods=['GET'], endpoint='get_gallery_image')
def get_gallery_image_rote(tbgallery_id):
    try:
        return get_gallery_image(tbgallery_id)
    except Exception as e:
        return jsonify({"error" : str(e)})

@gallery_bp.route('/gallery', methods=['GET'])
def get_gallery_route():
    """
    Получить данные галереи с учетом пагинации.

    Этот маршрут обрабатывает GET-запросы для получения данных галереи с учетом пагинации. Он извлекает параметры 'page'
    и 'per_page' из URL-строки, рассчитывает смещение и выполняет запрос к базе данных для извлечения данных галереи.
    Затем он создает список словарей для сериализации и возвращает JSON-ответ с данными галереи.

    Returns:
        jsonify({'gallery_data': gallery_list}): JSON-ответ с данными галереи.

    """
    try:        
        return get_gallery_data()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@gallery_bp.route('/gallery', methods=['GET'])
def get_gallery_by_route():
    try:        
        return get_gallery_data_by()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@gallery_bp.route('/gallery', methods=['POST'])
@login_required
def create_gallery():
    """
    Создать новую запись в галерее с загрузкой изображения.

    Этот маршрут обрабатывает POST-запросы для создания новой записи в галерее с загрузкой изображения. Он проверяет,
    было ли отправлено изображение в запросе, и если да, то сохраняет его на сервере и создает новую запись в галерее
    с соответствующей информацией. Затем он сохраняет запись в базе данных и возвращает JSON-ответ о результате операции.

    Returns:
        jsonify({'message': 'Запись успешно создана'}), 201: JSON-ответ об успешном создании записи.
        jsonify({'error': 'Изображение не было отправлено'}), 400: JSON-ответ об ошибке, если изображение не было отправлено.
        jsonify({'error': 'Недопустимое расширение файла изображения'}), 400: JSON-ответ об ошибке, если расширение файла не разрешено.

    """
    try:
        return create_gallery_info()
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@gallery_bp.route('/gallery/<uuid:tbgallery_id>', methods=['PUT'])
@login_required
def update_gallery(tbgallery_id):    
    try:
        return update_gallery_info(tbgallery_id)
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@gallery_bp.route('/gallery/<string:tbgallery_id>', methods=['DELETE'])
@login_required
def delete_gallery(tbgallery_id):
    """
    Удалить запись из галереи по идентификатору.

    Этот маршрут обрабатывает DELETE-запросы для удаления записи из галереи по указанному идентификатору `tbgallery_id`.
    Он ищет запись в галерее по указанному идентификатору. Если запись не найдена, маршрут возвращает JSON-ответ с ошибкой.
    Если запись найдена, то маршрут удаляет ее из базы данных и возвращает JSON-ответ о результате операции.

    Args:
        tbgallery_id (string): Идентификатор записи в галерее.

    Returns:
        jsonify({'message': 'Запись успешно удалена'}), 200: JSON-ответ об успешном удалении записи.
        jsonify({'error': 'Запись не найдена'}), 404: JSON-ответ об ошибке, если запись не найдена.

    """
    try:
        return delete_gallery_info(tbgallery_id)
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    
    
