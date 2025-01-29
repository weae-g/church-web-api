from flask import request, jsonify, Blueprint
from .services import (
    get_employee_image,
    create_employee,    
    get_employees,
    update_employee,
    delete_employee,
    get_employee,
    search_employee,   
    create_employee_image,
    delete_employee_image
)

employee_bp = Blueprint("employee", __name__)

@employee_bp.route('/employee_image/<employee_image_id>', methods=['GET'])
def get_employee_image_file(employee_image_id):
    try:
        return get_employee_image(employee_image_id=employee_image_id)
    except Exception as e:
        return ({"error" : str(e)})

@employee_bp.route("/employee/search_employee", methods=["GET", "POST"])
def get_employee_by_name():
    """
    Получить информацию о сотруднике по имени.

    Этот маршрут обрабатывает GET-запросы для поиска сотрудника по имени. Он принимает строку `search_name` в качестве
    параметра пути и ищет сотрудника с указанным именем. Если сотрудник найден, маршрут возвращает информацию о нем в формате
    JSON. Если сотрудник не найден, маршрут возвращает JSON-ответ с сообщением о том, что сотрудник с указанным именем не
    найден.

    Args:
        search_name (string): Имя сотрудника для поиска.

    Returns:
        jsonify(employee_info), 200: JSON-ответ с информацией о сотруднике, если сотрудник найден.
        jsonify({'message': 'Сотрудник с указанным именем не найден'}), 404: JSON-ответ, если сотрудник не найден.
        jsonify({"error" : str(e)}), 500: JSON-ответ об ошибке, если произошла ошибка при выполнении запроса.

    """
    try:
        return search_employee()
    except Exception as e:
        return jsonify({"erroe" : str(e)}), 500


@employee_bp.route("/employee", methods=["GET"])
def list_employers():
    """
    Получить список всех сотрудников.

    Этот маршрут обрабатывает GET-запросы для получения списка всех сотрудников. Он извлекает информацию о всех
    сотрудниках из базы данных и возвращает ее в формате JSON.

    Returns:
        jsonify(employees), 200: JSON-ответ с информацией о всех сотрудниках.
        jsonify({"error": str(e)}), 500: JSON-ответ об ошибке, если произошла ошибка при выполнении запроса.

    """
    try:
        return get_employees()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/employee/<uuid>", methods=["GET"])
def get_one_employee(uuid):
    """
    Получить информацию о сотруднике по идентификатору.

    Этот маршрут обрабатывает GET-запросы для получения информации о сотруднике по его идентификатору. Он извлекает
    информацию о сотруднике из базы данных, используя переданный идентификатор, и возвращает ее в формате JSON.

    Args:
        uuid (str): Уникальный идентификатор сотрудника.

    Returns:
        jsonify(employee), 200: JSON-ответ с информацией о сотруднике.
        jsonify({"error": str(e)}), 500: JSON-ответ об ошибке, если произошла ошибка при выполнении запроса.

    """
    try:
        return get_employee(uuid)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/employee/<uuid>", methods=["PUT"])
def update_one_employee(uuid):
    """
    Обновить информацию о сотруднике по идентификатору.

    Этот маршрут обрабатывает PUT-запросы для обновления информации о сотруднике по его идентификатору. Он извлекает
    информацию о сотруднике из запроса и пытается обновить ее в базе данных, используя переданный идентификатор. Если
    сотрудник с указанным идентификатором не найден, возвращается ошибка 404. В случае успешного обновления информации
    возвращается JSON-ответ с сообщением об успешном обновлении.

    Args:
        uuid (str): Уникальный идентификатор сотрудника.

    Returns:
        jsonify({"message": "Информация о сотруднике успешно обновлена"}), 200: JSON-ответ об успешном обновлении.
        jsonify({"error": "Сотрудник не найден"}), 404: JSON-ответ об ошибке, если сотрудник не найден.
        jsonify({"error": str(e)}), 500: JSON-ответ об ошибке, если произошла ошибка при выполнении запроса.

    """
    try:
        return update_employee(uuid)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/employee/<uuid>", methods=["DELETE"])
def delete_one_employee(uuid):
    """
    Удалить информацию о сотруднике по идентификатору.

    Этот маршрут обрабатывает DELETE-запросы для удаления информации о сотруднике по его уникальному идентификатору.
    Он извлекает идентификатор сотрудника из URL и пытается удалить информацию о сотруднике из базы данных. Если сотрудник
    с указанным идентификатором не найден, возвращается ошибка 404. В случае успешного удаления информации возвращается
    JSON-ответ с сообщением об успешном удалении.

    Args:
        uuid (str): Уникальный идентификатор сотрудника.

    Returns:
        jsonify({"message": "Информация о сотруднике успешно удалена"}), 200: JSON-ответ об успешном удалении.
        jsonify({"error": "Сотрудник не найден"}), 404: JSON-ответ об ошибке, если сотрудник не найден.
        jsonify({"error": str(e)}), 500: JSON-ответ об ошибке, если произошла ошибка при выполнении запроса.

    """
    try:
        return delete_employee(str(uuid))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/employee", methods=["POST"])
def create_one_employee():   
    try:
        return create_employee()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@employee_bp.route("/employee/upload_image", methods=["POST"])
def upload_image_employee():
    try:
        return create_employee_image()
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    
@employee_bp.route("/employee/delete_image/<uuid:id>", methods=["DELETE"])
def delete_image_employee(id):  
    try:
        return delete_employee_image(id)
    except Exception as e:
        return jsonify({"error": str(e)}), 500