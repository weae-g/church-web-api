from .models import Gallery, GalleryType
from .serialize import GallerySchema, GalleryTypeShema
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os, io
from create_app import db
from flask import send_file, url_for

GallerySchemas = GallerySchema(many=True)
GallerySchemasOne = GallerySchema(many=False)
GalleryTypeSchemas = GalleryTypeShema(many=True)


UPLOAD_FOLDER = 'uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


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


def get_gallery_data():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        start_number = (page - 1) * per_page + 1
        end_number = start_number + per_page
        selected_gallery = Gallery.query.filter(start_number <= Gallery.image_number, Gallery.image_number <= end_number).all()
        
        gallery_info = []
        for gallery in selected_gallery:
            image_url = f"/gallery/image/{str(gallery.tbgallery_id)}"  # Создаем URL для получения изображения.
            gallery_info.append({
                "tbgallery_id": str(gallery.tbgallery_id),
                "image_url": url_for('gallery.get_gallery_image', tbgallery_id=gallery.tbgallery_id),
                "date": gallery.date.isoformat(),
                "image_number": gallery.image_number,
                # Добавьте другие поля вашей модели Gallery в этот словарь.
            })
            
        return jsonify(gallery_info), 200
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500


def create_gallery_info():
    try:     
        gallery_type_id = request.form.get("gallery_type_id")
        images = request.files.getlist('pictures')

        for image in images:
            image_data = image.read()
            max_image_number = db.session.query(db.func.max(Gallery.image_number)).scalar()

            if max_image_number is None:
                max_image_number = 1
            else:
                max_image_number += 1

            # Создайте новую запись галереи для каждого изображения
            gallery = Gallery(
                image_number=max_image_number,
                image=image_data,
                gallery_type_id=gallery_type_id
            )

            # Добавьте запись в базу данных
            db.session.add(gallery)

        db.session.commit()

        return jsonify({"message": "Изображеие успешноо отправлено"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_gallery_info(tbgallery_id):
    try:
        gallery = Gallery.query.filter_by(tbgallery_id=tbgallery_id).first()

        if not gallery:
            return jsonify({'Ошибка': 'Элемент галереи не найден'}), 404

        gallery_type_id = request.form.get("gallery_type_id")
        new_image = request.files.get('new_image')

        if new_image:
            image_data = new_image.read()
            gallery.image = image_data

        if gallery_type_id:
            gallery.gallery_type_id = gallery_type_id

        db.session.commit()

        return jsonify({"message": "Изображение успешно заменено"}), 200
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
