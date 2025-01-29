from flask import request, jsonify, Blueprint
from flask_login import login_required
from .services import (
    get_timetable_and_employees_all_info,
    get_timetable_and_employees_all_info_two,
    get_timetable_and_employees_info,
    update_timetable_info,
    create_timetable_info,
    delete_timetable_info,
    create_timetable_employee_info,
    delete_timetable_employee_info,   
    update_timetable_employee_info
)

timetable_bp = Blueprint("timetable", __name__)

@timetable_bp.route("/timetable", methods=["GET"])
def get_timetable_and_employees():
    """
    Получить расписание и информацию о сотрудниках.

    Эта функция отправляет GET-запрос для получения информации о расписании и сотрудниках.
    Она вызывает функцию get_timetable_and_employees_all_info() для получения данных и возвращает их.

    Возвращает:
        Response: JSON-ответ, содержащий информацию о расписании и сотрудниках.

    Исключения:
        Exception: В случае возникновения ошибки при получении информации, возбуждается исключение.
            Исключение перехватывается, и возвращается ответ с кодом состояния 500 (Внутренняя ошибка сервера).

    Пример использования:
        Чтобы получить информацию о расписании и сотрудниках, сделайте GET-запрос к конечной точке "/timetable".

    Примечание:
        Эта функция является частью веб-приложения Flask, использующего фреймворк Flask-RESTful.

    """
    try:
        return get_timetable_and_employees_all_info()
    except Exception as e:
        return e, 500

@timetable_bp.route("/timetable/all", methods=["GET"])
def get_timetable_and_employees_route():
    """
    Получить расписание и информацию о сотрудниках.

    Эта функция отправляет GET-запрос для получения информации о расписании и сотрудниках.
    Она вызывает функцию get_timetable_and_employees_all_info() для получения данных и возвращает их.

    Возвращает:
        Response: JSON-ответ, содержащий информацию о расписании и сотрудниках.

    Исключения:
        Exception: В случае возникновения ошибки при получении информации, возбуждается исключение.
            Исключение перехватывается, и возвращается ответ с кодом состояния 500 (Внутренняя ошибка сервера).

    Пример использования:
        Чтобы получить информацию о расписании и сотрудниках, сделайте GET-запрос к конечной точке "/timetable".

    Примечание:
        Эта функция является частью веб-приложения Flask, использующего фреймворк Flask-RESTful.

    """
    try:
        return get_timetable_and_employees_all_info_two()
    except Exception as e:
        return e, 500

@timetable_bp.route("/timetable/<uuid:tbtimetable_id>", methods=["GET"])
def get_timetable_and_employees_all(tbtimetable_id):
    """
    Получить информацию о расписании и сотрудниках по указанному идентификатору расписания.

    Эта функция отправляет GET-запрос для получения информации о расписании и сотрудниках,
    используя уникальный идентификатор расписания (tbtimetable_id) в качестве параметра.

    Аргументы:
        tbtimetable_id (uuid): Уникальный идентификатор расписания в формате UUID.

    Возвращает:
        Response: JSON-ответ, содержащий информацию о расписании и сотрудниках, связанную с указанным идентификатором.

    Исключения:
        Exception: В случае возникновения ошибки при получении информации, возбуждается исключение.
            Исключение перехватывается, и возвращается ответ с кодом состояния 500 (Внутренняя ошибка сервера).

    Пример использования:
        Чтобы получить информацию о расписании и сотрудниках по идентификатору UUID, сделайте GET-запрос
        к конечной точке "/timetable/<uuid:tbtimetable_id>", где tbtimetable_id заменяется фактическим UUID.

    Примечание:
        Эта функция является частью веб-приложения Flask, использующего фреймворк Flask-RESTful.

    """
    try:
        return get_timetable_and_employees_info(tbtimetable_id)
    except Exception as e:
        return e, 500

@timetable_bp.route('/timetable/<time_table_id>/<employee_id>', methods=['PUT'])
@login_required
def update_timetable_employee_info_route(time_table_id, employee_id):
    try:
        update_timetable_employee_info(time_table_id, employee_id)
    except Exception as e:
        return jsonify({"error" : str(e)})
       
@timetable_bp.route("/timetable/<uuid:tbtimetable_id>", methods=["PUT"])
@login_required
def update_timetable(tbtimetable_id):
    try:
        return update_timetable_info(tbtimetable_id)
    except Exception as e:
        return e, 500

@timetable_bp.route("/timetable", methods=["POST"])
@login_required
def create_timetable():
    """
    Создать новое расписание.

    Эта функция отправляет POST-запрос для создания нового расписания.
    Возвращает информацию о созданном расписании и код состояния 201 (Создан).

    Возвращает:
        Response: JSON-ответ с информацией о созданном расписании и кодом состояния 201 (Создан).

    Исключения:
        Exception: В случае возникновения ошибки при создании расписания, возбуждается исключение.
            В этом случае, возвращается JSON-ответ с сообщением об ошибке и кодом состояния 500 (Внутренняя ошибка сервера).

    Пример использования:
        Чтобы создать новое расписание, сделайте POST-запрос к конечной точке "/timetable".
        В теле запроса отправьте данные, необходимые для создания нового расписания.

    Примечание:
        Эта функция является частью веб-приложения Flask, использующего фреймворк Flask-RESTful.

    """
    try:
        return create_timetable_info()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@timetable_bp.route("/timetable/<uuid>", methods=["DELETE"])
@login_required
def delete_timetable_by_id(uuid):
    """
    Удалить расписание по указанному уникальному идентификатору (UUID).

    Эта функция отправляет DELETE-запрос для удаления расписания с использованием
    указанного уникального идентификатора (UUID) в качестве параметра.

    Аргументы:
        uuid (uuid): Уникальный идентификатор расписания в формате UUID.

    Возвращает:
        Response: JSON-ответ, подтверждающий успешное удаление расписания.

    Исключения:
        Exception: В случае возникновения ошибки при удалении расписания, возбуждается исключение.
            В этом случае, возвращается JSON-ответ с сообщением об ошибке и кодом состояния 500 (Внутренняя ошибка сервера).

    Пример использования:
        Чтобы удалить расписание по уникальному идентификатору UUID, сделайте DELETE-запрос
        к конечной точке "/timetable/<uuid>", где uuid заменяется фактическим UUID.

    Примечание:
        Эта функция является частью веб-приложения Flask, использующего фреймворк Flask-RESTful.

    """
    try:
        return delete_timetable_info(uuid)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@timetable_bp.route("/timetable/employee", methods=["POST"])
@login_required
def create_timetable_employee():
    """
    Создать новую запись о сотруднике в расписании.

    Эта функция отправляет POST-запрос для создания новой записи о сотруднике в расписании.
    Возвращает информацию о созданной записи и код состояния 201 (Создан).

    Возвращает:
        Response: JSON-ответ с информацией о созданной записи и кодом состояния 201 (Создан).

    Исключения:
        Exception: В случае возникновения ошибки при создании записи о сотруднике, возбуждается исключение.
            В этом случае, возвращается JSON-ответ с сообщением об ошибке и кодом состояния 500 (Внутренняя ошибка сервера).

    Пример использования:
        Чтобы создать новую запись о сотруднике в расписании, сделайте POST-запрос к конечной точке "/timetable/employee".
        В теле запроса отправьте данные, необходимые для создания новой записи.

    Примечание:
        Эта функция является частью веб-приложения Flask, использующего фреймворк Flask-RESTful.

    """
    try:
        return create_timetable_employee_info()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@timetable_bp.route("/timetable/employee/<uuid>", methods=["DELETE"])
@login_required
def delete_timetable_employee_by_id(uuid):
    """
    Удалить запись о сотруднике в расписании по указанному уникальному идентификатору (UUID).

    Эта функция отправляет DELETE-запрос для удаления записи о сотруднике в расписании с использованием
    указанного уникального идентификатора (UUID) в качестве параметра.

    Аргументы:
        uuid (uuid): Уникальный идентификатор записи о сотруднике в формате UUID.

    Возвращает:
        Response: JSON-ответ, подтверждающий успешное удаление записи о сотруднике.

    Исключения:
        Exception: В случае возникновения ошибки при удалении записи о сотруднике, возбуждается исключение.
            В этом случае, возвращается JSON-ответ с сообщением об ошибке и кодом состояния 500 (Внутренняя ошибка сервера).

    Пример использования:
        Чтобы удалить запись о сотруднике в расписании по уникальному идентификатору UUID,
        сделайте DELETE-запрос к конечной точке "/timetable/employee/<uuid>", где uuid заменяется фактическим UUID.

    Примечание:
        Эта функция является частью веб-приложения Flask, использующего фреймворк Flask-RESTful.

    """
    try:
        return delete_timetable_employee_info(uuid)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

