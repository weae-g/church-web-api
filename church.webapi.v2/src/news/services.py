from .models import News, NewsType, NewsImage
from .serialize import NewsSchema
from flask import request, jsonify, url_for ,send_file
from sqlalchemy import desc
from flask import session
import uuid, sys, io
import xml.etree.ElementTree as ET
import requests
sys.path.append(sys.path[0][:-5])
from create_app import db

NewsSchemas = NewsSchema(many=True)
NewsSchemasOne = NewsSchema(many=False)

def get_news_at_russ():
    """
    Получить новости с RSS-ленты "Патриархия.ру".

    Функция выполняет запрос к RSS-ленте и извлекает информацию о новостях, включая заголовок, описание, ссылку,
    URL вложения (если есть) и дату публикации.

    Returns:
        jsonify(data): JSON-ответ с данными о новостях.

    """
    url = 'http://www.patriarchia.ru/rss/rss_news.rss'
    response = requests.get(url)
    if response.status_code == 200:
        xml_data = response.text
        root = ET.fromstring(xml_data)

        data = []

        # Извлекаем заголовки, описания, ссылки и даты публикации новостей из RSS-ленты
        for item in root.findall('.//item'):
            title = item.find('title').text
            description = item.find('description').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text  # Извлекаем дату публикации
            
            enclosure = item.find('enclosure')
            if enclosure is not None:
                enclosure_url = enclosure.get('url')
            else:
                enclosure_url = None
                
            data.append({"title" : title, "description" : description, "link" : link, "url" : enclosure_url, "pub_date": pub_date})
        
        return jsonify(data)
    else:
        return {"Ошибка при загрузке данных:", response.status_code}

def search_news_by_date():
    """
    Поиск новостей по дате.

    Функция выполняет поиск новостей в базе данных по заданной дате и возвращает информацию о найденных новостях в формате JSON.

    Args:
        None (параметр даты передается через query параметры).

    Returns:
        JSON: Информация о найденных новостях в формате JSON.

    Raises:
        404: Если новости не найдены.
        500: Если возникла ошибка при выполнении запроса.

    Example:
        Если вы передадите `date` в запросе, например, через URL-параметры,
        функция выполнит поиск новостей по указанной дате и вернет результат в формате JSON.

    """
    try:
        selected_news = News.query.filter_by(news_date=request.args.get('date')).all()
        news_info = []

        if selected_news:
            for news in selected_news:
                images = news.news_image
                image_urls = [url_for('news.get_image', image_id=image.id) for image in images]

                news_info.append({
                    "news_id": news.news_id,
                    "news_type_id": news.news_type_id,
                    "news_title": news.news_title,
                    "news_date": news.news_date,
                    "news_description": news.news_description,
                    "news_number": news.news_number,
                    "news_image": {
                        "image_urls": image_urls,
                    },
                    "news_type": {
                        "type_name": news.news_type.type_name
                    },
                })

            return jsonify(news_info), 200
        else:
            return jsonify({'Ошибка': 'Новости не найдены'}), 404
    except Exception as e:
        return jsonify({'Ошибка': str(e)}), 500

def search_news_by_name():
    """
    Поиск новостей по имени.

    Функция выполняет поиск новостей в базе данных по заданному имени новости и возвращает информацию о найденных новостях в формате JSON.

    Args:
        None (имя новости передается через query параметры).

    Returns:
        JSON: Информация о найденных новостях в формате JSON.

    Raises:
        404: Если новости не найдены.
        500: Если возникла ошибка при выполнении запроса.

    Example:
        Если вы передадите `name` в запросе, например, через URL-параметры,
        функция выполнит поиск новостей с указанным именем и вернет результат в формате JSON.

    """
    try:
        search_name = request.args.get('name') 
        selected_news = News.query.filter(News.news_title.contains(search_name)).all()
        news_info = []

        if selected_news:
            for news in selected_news:
                images = news.news_image
                image_urls = [url_for('news.get_image', image_id=image.id) for image in images]

                news_info.append({
                    "news_id": news.news_id,
                    "news_type_id": news.news_type_id,
                    "news_title": news.news_title,
                    "news_date": news.news_date,
                    "news_description": news.news_description,
                    "news_number": news.news_number,
                    "news_image": {
                        "image_urls": image_urls,
                    },
                    "news_type": {
                        "type_name": news.news_type.type_name
                    },
                })

            return jsonify(news_info), 200
        else:
            return jsonify({'Ошибка': 'Новости не найдены'}), 404
    except Exception as e:
        return jsonify({'Ошибка': str(e)}), 500

def get_image_collection(image_id):
    """
    Получает изображение из коллекции по его уникальному идентификатору (image_id).

    :param image_id: Уникальный идентификатор изображения.
    :type image_id: str
    :return: Если изображение найдено, возвращает изображение в формате JPEG и код состояния 200 OK.
             Если изображение не найдено, возвращает сообщение об ошибке 404 Not Found.
    :rtype: tuple
    """
    image = NewsImage.query.filter(NewsImage.id == image_id).first()

    if not image:
        return f"Изображение не найдено id: {image_id}", 404

    mime_type = "image/jpeg"

    return send_file(io.BytesIO(image.image_data), mimetype=mime_type), 200

def get_one_news(id):
    """
    Получает информацию о одной новости по ее уникальному идентификатору (id).

    :param id: Уникальный идентификатор новости.
    :type id: str
    :return: Если новость найдена, возвращает информацию о новости и ее фотографиях в формате JSON
             и код состояния 200 OK. Если новость не найдена, возвращает сообщение об ошибке 404 Not Found.
             Если возникает ошибка при выполнении запроса, возвращает сообщение об ошибке 500 Internal Server Error.
    :rtype: tuple
    """
    try:
        selected_news = News.query.get(id)
        news_info = []
        images = selected_news.news_image

        image_urls = [url_for('news.get_image', image_id=image.id) for image in images]

        news_info = {
            "news_id": selected_news.news_id,
            "news_type_id": selected_news.news_type_id,
            "news_title": selected_news.news_title,
            "news_date": selected_news.news_date,
            "news_description": selected_news.news_description,
            "news_number": selected_news.news_number,
            "news_image": {
                "image_urls": image_urls,
            },
            "news_type": {
                "type_name": selected_news.news_type.type_name
            },
        }

        return jsonify(news_info), 200
    except Exception as e:
        return jsonify({'Ошибка': str(e)}), 500

def get_last(count):
    """
    Получает указанное количество последних новостей из базы данных.

    Args:
        count (int): Количество новостей, которое необходимо получить.

    Returns:
        tuple: Кортеж, содержащий JSON-ответ с информацией о новостях и код состояния HTTP.

            - Если операция выполнена успешно, возвращается кортеж (JSON, 200).
            - Если произошла ошибка, возвращается кортеж (JSON с сообщением об ошибке, 500).

    Example:
        # Получить последние 10 новостей
        result = get_last(10)
    """
    try:       
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        start_number = (page - 1) * per_page + 1
        end_number = start_number + per_page
        selected_news = News.query.order_by(desc(News.news_date)).limit(count).all()
        news_info = []
        for news in selected_news:
            images = news.news_image
            image_urls = [url_for('news.get_image', image_id=image.id) for image in images]
            news_info.append({
                "news_id": news.news_id,
                "news_type_id": news.news_type_id,
                "news_title": news.news_title,
                "news_date": news.news_date,
                "news_description": news.news_description,
                "news_number": news.news_number,
                "news_image": {
                    "image_urls": image_urls,
                },
                "news_type": {
                    "type_name": news.news_type.type_name
                },
            })
            
        return jsonify(news_info), 200
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500

def get_list_news():
    """
    Получает список новостей с пагинацией и возвращает информацию о них в формате JSON.

    :return: Если новости найдены, возвращает информацию о новостях в формате JSON и код состояния 200 OK.
             Если возникает ошибка при выполнении запроса, возвращает сообщение об ошибке 500 Internal Server Error.
    :rtype: tuple
    """
    try:       
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        start_number = (page - 1) * per_page + 1
        end_number = start_number + per_page
        selected_news = News.query.filter(start_number <= News.news_number, News.news_number <= end_number).order_by(desc(News.news_date)).all()
        news_info = []
        for news in selected_news:
            images = news.news_image
            image_urls = [url_for('news.get_image', image_id=image.id) for image in images]
            news_info.append({
                "news_id": news.news_id,
                "news_type_id": news.news_type_id,
                "news_title": news.news_title,
                "news_date": news.news_date,
                "news_description": news.news_description,
                "news_number": news.news_number,
                "news_image": {
                    "image_urls": image_urls,
                },
                "news_type": {
                    "type_name": news.news_type.type_name
                },
            })
            
        return jsonify(news_info), 200
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500
   
def get_all_news_count():
    """
    Получает количество всех новостей в базе данных и возвращает его в формате JSON.

    :return: Если количество новостей успешно получено, возвращает количество в формате JSON и код состояния 200 OK.
             Если возникает ошибка при выполнении запроса, возвращает сообщение об ошибке 500 Internal Server Error.
    :rtype: tuple
    """
    try:
        items = News.query.all()
        response = NewsSchemas.dump(items)
        return {"Количество: ": len(response)}, 200
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500
    
def get_news_by_type():
    """
    Получает список новостей определенного типа с пагинацией.

    Args:
        request.form['page'] (int): Номер страницы для пагинации.
        request.form['per_page'] (int): Количество элементов на странице.
        request.form['type_id'] (str): Идентификатор типа новостей для фильтрации.

    Returns:
        tuple: Возвращает JSON-ответ, содержащий список новостей указанного типа с
        пагинацией и информацию о каждой новости, включая изображения и тип.

    Raises:
        Exception: Если произошла ошибка во время выполнения запроса, возвращает
        500 Internal Server Error с описанием ошибки.
    """
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        type_name = request.args.get("type_name")
        start_number = (page - 1) * per_page + 1
        end_number = start_number + per_page
        selected_news = News.query.filter(
            start_number <= News.news_number, 
            News.news_number <= end_number,
            NewsType.type_name == type_name)
        news_info = []
        for news in selected_news:
            images = news.news_image 
            image_urls = [url_for('news.get_image', image_id=image.id) for image in images]
            news_info.append({
                "news_id": news.news_id,
                "news_type_id": news.news_type_id,
                "news_title": news.news_title,
                "news_date": news.news_date,
                "news_description": news.news_description,
                "news_number": news.news_number,
                "news_image": {
                    "image_urls": image_urls,
                },
                "news_type": {
                    "type_name": news.news_type.type_name
                },
            })
        return jsonify(news_info), 200
    except Exception as e:
        print(e)
        return jsonify({"Ошибка": str(e)}), 500

def create_news():
    """
    Создает новость на основе данных, полученных из запроса, и добавляет изображения к новости, если они имеются.

    :return: Сообщение об успешном создании новости или сообщение об ошибке.
    :rtype: dict
    """
    try:
        max_news_number = db.session.query(db.func.max(News.news_number)).scalar()

        if max_news_number is None:
            max_news_number = 1
        else:
            max_news_number += 1
        
        news_data = {
            "news_type_id": request.form.get("news_type_id"),
            "news_title": request.form.get("news_title"),
            "news_number" : max_news_number,
            "news_description": request.form.get("news_description"),
        }

        news = News(**news_data)

        images = request.files.getlist('pictures')

        if images:
            for picture in images:
                if picture:
                    img = NewsImage(
                        image_data=picture.read(),
                        mimetype=picture.mimetype,
                        name=picture.filename
                    )
                    news.news_image.append(img)

        db.session.add(news)
        db.session.commit()

        return jsonify({"message": "Новость успешно созданна"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_news_image():
    """
    Создает изображение новости на основе данных, полученных из запроса.

    :return: Сообщение об успешном создании изображения новости или сообщение об ошибке.
    :rtype: dict
    """
    try:
        image_data = request.files.get('image_data')
        mimetype = image_data.mimetype
        name = image_data.filename
        news_id_fk = request.form.get('news_id_fk')

        if not image_data:
            return jsonify({"error": "Изображение не предоставлено"}), 400

        new_image = NewsImage(
            image_data=image_data.read(),
            mimetype=mimetype,
            name=name,
            news_id_fk=news_id_fk
        )

        db.session.add(new_image)
        db.session.commit()

        return jsonify({"message": "Изображение новости успешно создано"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def upload_image_to_news(id):
    """
    Загружает изображение и привязывает его к новости с указанным ID.

    :param id: ID новости, к которой нужно привязать изображение.
    :type id: str
    :return: Сообщение об успешной загрузке изображения или сообщение об ошибке.
    :rtype: dict
    """
    try:
        picture = request.files['picture']

        if not picture:
            return jsonify({"error": "Нету изображения для загрузки"}), 400

        img = NewsImage(id=uuid.uuid4(), image_data=picture.read(), mimetype=picture.mimetype, name=picture.filename, news_id_fk=id)

        db.session.add(img)
        db.session.commit()

        return jsonify({"message": "Изображение успешно загружено"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
def update_news_image(image_id):
    """
    Обновляет данные о изображении на основе переданных данных.

    :param image_id: ID изображения, которое нужно обновить.
    :type image_id: str
    :param updated_data: Словарь с данными для обновления.
    :type updated_data: dict
    :return: Сообщение об успешном обновлении изображения или сообщение об ошибке.
    :rtype: dict
    """
    try:
        image = NewsImage.query.get(image_id)
        if image is None:
            return jsonify({"message": "Image not found"}), 404

        images = request.files.getlist('pictures')

        if images:
            for picture in images:
                if picture:
               
                    image.image_data = picture.read()

        db.session.commit()
        return jsonify({"message": "Изображение успешно изменено"}), 200
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500


def update_news(news_id):
    try:   
        news = News.query.get(news_id)
        if news is None:
            return {"message": "Новость не найдена"}, 404

        news_title = request.form.get("news_title")
        news_description = request.form.get("news_description")
        news_date = request.form.get("news_date")

        if news_title is not None:
            news.news_title = news_title
        if news_description is not None:
            news.news_description = news_description
        if news_date is not None:
            news.news_date = news_date


        uploaded_files = request.files.getlist("images")

     
        for uploaded_file in uploaded_files:
            new_image = NewsImage(image_data=uploaded_file.read(),
                                  mimetype=uploaded_file.mimetype,
                                  name=uploaded_file.filename,
                                  news_id_fk=news_id)
            db.session.add(new_image)

        db.session.commit()

        return {"message": "Новость успешно изменена"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

def delete_news_by_id(id):
    """
    Удаляет новость и связанные с ней изображения из базы данных по заданному ID.

    :param id: ID новости для удаления.
    :type id: str
    :return: Сообщение об успешном удалении новости.
    :rtype: str
    """
    NewsImage.query.filter_by(news_id_fk=id).delete()
    News.query.filter_by(news_id=id).delete()
    db.session.commit()
    return f'Модель с id "{id}" была успешно удалена!'

def delete_news_image_by_id(id):
    """
    Удаляет новость и связанные с ней изображения из базы данных по заданному ID.

    :param id: ID новости для удаления.
    :type id: str
    :return: Сообщение об успешном удалении новости.
    :rtype: str
    """
    NewsImage.query.filter_by(id=id).delete()
    db.session.commit()
    return f'Фотография с "{id}" была успешно удалена!'

