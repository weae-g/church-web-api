from .models import Gallery, GalleryType, Album
from .serialize import GallerySchema, GalleryTypeShema, AlbumSchema, GallerySchemaOnse
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os, io
from create_app import db
from flask import send_file, url_for
import random

GallerySchemas = GallerySchema(many=True)
GallerySchemasOne = GallerySchema(many=False)
GalleryTypeSchemas = GalleryTypeShema(many=True)

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)

UPLOAD_FOLDER = 'uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#region album

def create_album():
    try:
        name = request.json['name']
        description = request.json.get('description', None)

        new_album = Album(name=name, description=description)
        db.session.add(new_album)
        db.session.commit()

        return jsonify({'message': 'Альбом успешно создан'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_album(album_id):
    try:
        album = Album.query.get(album_id)
        if not album:
            return jsonify({'error': 'Альбом не найден'}), 404
        
        result = album_schema.dump(album)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_all_albums():
    try:
        albums = Album.query.all()
        result = albums_schema.dump(albums)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def update_album(album_id):
    try:
        album = Album.query.get(album_id)
        if not album:
            return jsonify({'error': 'Альбом не найден'}), 404
        
        name = request.json.get('name', album.name)
        description = request.json.get('description', album.description)

        album.name = name
        album.description = description

        db.session.commit()

        return jsonify({'message': 'Альбом успешно обновлен'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_album(album_id):
    try:
        album = Album.query.get(album_id)
        if not album:
            return jsonify({'error': 'Альбом не найден'}), 404
        
        db.session.delete(album)
        db.session.commit()

        return jsonify({'message': 'Альбом успешно удален'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#endregion

def allowed_file(filename):
    """
    Проверяет, разрешено ли загружать файл с заданным расширением.

    Args:
        filename (str): Имя файла.

    Returns:
        bool: True, если загрузка файла с указанным расширением разрешена, иначе False.

    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_pathc():
    """
    Получает путь к текущему каталогу, где находится файл, в котором она вызвана.

    Returns:
        str: Путь к текущему каталогу.

    """
    return os.path.dirname(__file__)


def get_gallery_image(tbgallery_id):
    try:
        gallery = Gallery.query.get(tbgallery_id)

        if not gallery:
            return jsonify({"message": "Изображение не найдено"}), 404

        # Отправка изображения как файла.
        return send_file(io.BytesIO(gallery.image), mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500

def delete_album(album_id):
    try:
        # Ищем альбом по переданному album_id
        album = Album.query.filter_by(id=album_id).first()
        
        # Если альбом не найден, возвращаем ошибку
        if not album:
            return jsonify({"Ошибка": "Альбом не найден"}), 404
        
        # Ищем все фотографии, связанные с альбомом
        galleries = Gallery.query.filter_by(album_id=album_id).all()
        
        # Удаляем все фотографии
        for gallery in galleries:
            db.session.delete(gallery)
        
        # Удаляем альбом
        db.session.delete(album)
        
        # Сохраняем изменения в базе данных
        db.session.commit()
        
        return jsonify({"Сообщение": "Альбом и все связанные с ним фотографии успешно удалены"}), 200
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500

def get_gallery_data_by():
    try:
        # Получаем параметры запроса
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        album_id = request.args.get('album_id')
        gallery_type_id = request.args.get('gallery_type_id')

        # Рассчитываем начальный и конечный номер изображения
        start_number = (page - 1) * per_page + 1
        end_number = start_number + per_page - 1

        # Строим базовый запрос
        query = Gallery.query

        # Фильтруем по album_id, если он указан
        if album_id:
            query = query.filter(Gallery.album_id == album_id)

        # Фильтруем по gallery_type_id, если он указан
        if gallery_type_id:
            query = query.filter(Gallery.gallery_type_id == gallery_type_id)

        # Фильтруем по image_number
        query = query.filter(Gallery.image_number >= start_number, Gallery.image_number <= end_number)

        # Выполняем запрос
        selected_gallery = query.all()

        # Сериализуем данные
        gallery_info = GallerySchemas.dump(selected_gallery)

        return jsonify(gallery_info), 200
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500


def get_gallery_data():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        start_number = (page - 1) * per_page + 1
        end_number = start_number + per_page

        selected_galleries = Gallery.query.filter(Gallery.image_number.between(start_number, end_number)).all()

        albums = {}
        for gallery in selected_galleries:
            album_id = gallery.album_id
            if album_id not in albums:
                albums[album_id] = {
                    'id': album_id,
                    'name': gallery.album.name,
                    'description': gallery.album.description,
                    'galleries': []
                }
            albums[album_id]['galleries'].append(GallerySchemaOnse().dump(gallery))

        album_list = [value for value in albums.values()]
        
        return jsonify(album_list), 200
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500


def get_random_photos():
    try:
        galleries = Gallery.query.all()
        if len(galleries) < 5:
            return jsonify({"error": "Not enough photos in the gallery"}), 400
        random_galleries = random.sample(galleries, 5)
        return jsonify([GallerySchemasOne.dump(gallery) for gallery in random_galleries]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def create_gallery_info():
    try:
        gallery_type_id = request.form.get("gallery_type_id")
        album_id = request.form.get("album_id")
        images = request.files.getlist('pictures')

        for image in images:
            image_data = image.read()
            max_image_number = db.session.query(db.func.max(Gallery.image_number)).scalar() or 0
            max_image_number += 1

            gallery = Gallery(
                image_number=max_image_number,
                image=image_data,
                gallery_type_id=gallery_type_id,
                album_id=album_id
            )

            db.session.add(gallery)

        db.session.commit()

        return jsonify({"message": "Изображения успешно отправлены"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_gallery_info(tbgallery_id):
    try:
        gallery = Gallery.query.filter_by(tbgallery_id=tbgallery_id).first()

        if not gallery:
            return jsonify({'Ошибка': 'Элемент галереи не найден'}), 404

        gallery_type_id = request.form.get("gallery_type_id")
        album_id = request.form.get("album_id")
        new_image = request.files.get('new_image')

        if new_image:
            image_data = new_image.read()
            gallery.image = image_data

        if gallery_type_id:
            gallery.gallery_type_id = gallery_type_id

        if album_id:
            gallery.album_id = album_id

        db.session.commit()

        return jsonify({"message": "Изображение успешно обновлено"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def delete_gallery_info(tbgallery_id):
    """
    Удаляет запись из галереи по идентификатору.

    Функция ищет запись в галерее по указанному идентификатору `tbgallery_id`. Если запись не найдена, функция возвращает
    JSON-ответ с ошибкой. Если запись найдена, то функция удаляет ее из базы данных и возвращает JSON-ответ о результате
    операции.

    Args:
        tbgallery_id (int): Идентификатор записи в галерее.

    Returns:
        jsonify({'message': 'Запись успешно удалена'}), 200: JSON-ответ об успешном удалении записи.
        jsonify({'error': 'Запись не найдена'}), 404: JSON-ответ об ошибке, если запись не найдена.

    """
    gallery = Gallery.query.get(tbgallery_id)

    if gallery is None:
        return jsonify({'error': 'Запись не найдена'}), 404

    db.session.delete(gallery)
    db.session.commit()

    return jsonify({'message': 'Запись успешно удалена'}), 200
