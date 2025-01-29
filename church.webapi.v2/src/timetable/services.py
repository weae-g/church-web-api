from .models import TimeTable, TimeTableEmployee
from .serialize import TimeTableSchema, TimeTableEmployeeSchema
from flask import request, jsonify, url_for
import uuid, sys
from sqlalchemy import desc
from datetime import datetime, timedelta
sys.path.append(sys.path[0][:-5])
from create_app import db
import requests

TimeTableSchemas = TimeTableSchema(many=True)
TimeTableEmployeeSchemas = TimeTableEmployeeSchema(many=True)

def get_timetable_and_employees_info(tbtimetable_id):
    try:
        timetable = TimeTable.query.get(tbtimetable_id)
        if timetable is None:
            return jsonify({"message": "Расписание с таким иденификатором не найдено"}), 404

        timetable_data = {
            "tbtimetable_id": str(timetable.tbtimetable_id),
            "tbtimetable_date": timetable.tbtimetable_date.strftime("%Y-%m-%d %H:%M:%S"),
            "tbtimetable_duty": timetable.tbtimetable_duty,
            "tbtimetable_name": timetable.tbtimetable_name,
            "timetable_time": str(timetable.timetable_time),
        }

        employees = TimeTableEmployee.query.filter_by(time_table_id=tbtimetable_id).all()
        employee_data = [{"id": employee.id, "name": employee.name} for employee in employees]

        response_data = {
            "timetable": timetable_data,
            "employees": employee_data
        }

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_timetable_and_employees_all_info_two():
    try:
        #current_date = datetime.now().date()
        #end_date = current_date + timedelta(days=7)
        
        #all_timetables = TimeTable.query.filter(TimeTable.tbtimetable_date >= current_date, TimeTable.tbtimetable_date <= end_date).order_by(TimeTable.tbtimetable_date).all()
        #all_timetables = TimeTable.query.filter(TimeTable.tbtimetable_date >= current_date).order_by(TimeTable.tbtimetable_date).all()     
        all_timetables = TimeTable.query.order_by(TimeTable.tbtimetable_date.desc()).all()
        
        timetables_data = {}

        for timetable in all_timetables:
            date_str = timetable.tbtimetable_date.strftime("%Y-%m-%d")
            if date_str not in timetables_data:
                timetables_data[date_str] = []

            timetable_data = {
                "tbtimetable_id": str(timetable.tbtimetable_id),
                "tbtimetable_date": date_str,
                "tbtimetable_name": timetable.tbtimetable_name,
                "timetable_time": str(timetable.timetable_time),
            }

            if timetable.tbtimetable_duty is not None:
                timetable_data["tbtimetable_duty"] = timetable.tbtimetable_duty

            employees = TimeTableEmployee.query.filter_by(time_table_id=timetable.tbtimetable_id).all()
            employee_data = []

            for employee in employees:
                try:
                    response = requests.post('http://127.0.0.1:5000/api/employee/search_employee', data={'search_text': employee.name})

                    response.raise_for_status()
                    if response.status_code == 200:
                        employee_data.append({"id": employee.id, "name": employee.name, "data": response.json()})
                    else:
                        employee_data.append({"id": employee.id, "name": employee.name, "data": None})
                except requests.exceptions.RequestException as e:
                    employee_data.append({"id": employee.id, "name": employee.name, "data": None})
                except Exception as e:
                    employee_data.append({"id": employee.id, "name": employee.name, "data": None})

            response_data = {
                "timetable": timetable_data,
                "employees": employee_data
            }
            timetables_data[date_str].append(response_data)

        return jsonify(timetables_data), 200
    except Exception as e:
        return jsonify({"error" : str(e)})


def get_timetable_and_employees_all_info():
    try:
        current_date = datetime.now().date()
        end_date = current_date + timedelta(days=7)
        
        all_timetables = TimeTable.query.filter(TimeTable.tbtimetable_date >= current_date, TimeTable.tbtimetable_date <= end_date).order_by(TimeTable.tbtimetable_date).all()
        #all_timetables = TimeTable.query.filter(TimeTable.tbtimetable_date >= current_date).order_by(TimeTable.tbtimetable_date).all()     
        #all_timetables = TimeTable.query.order_by(TimeTable.tbtimetable_date.desc()).all()
        
        timetables_data = {}

        for timetable in all_timetables:
            date_str = timetable.tbtimetable_date.strftime("%Y-%m-%d")
            if date_str not in timetables_data:
                timetables_data[date_str] = []

            timetable_data = {
                "tbtimetable_id": str(timetable.tbtimetable_id),
                "tbtimetable_date": date_str,
                "tbtimetable_name": timetable.tbtimetable_name,
                "timetable_time": str(timetable.timetable_time),
            }

            if timetable.tbtimetable_duty is not None:
                timetable_data["tbtimetable_duty"] = timetable.tbtimetable_duty

            employees = TimeTableEmployee.query.filter_by(time_table_id=timetable.tbtimetable_id).all()
            employee_data = []

            for employee in employees:
                try:
                    response = requests.post('http://127.0.0.1:5000/api/employee/search_employee', data={'search_text': employee.name})

                    response.raise_for_status()
                    if response.status_code == 200:
                        employee_data.append({"id": employee.id, "name": employee.name, "data": response.json()})
                    else:
                        employee_data.append({"id": employee.id, "name": employee.name, "data": None})
                except requests.exceptions.RequestException as e:
                    employee_data.append({"id": employee.id, "name": employee.name, "data": None})
                except Exception as e:
                    employee_data.append({"id": employee.id, "name": employee.name, "data": None})

            response_data = {
                "timetable": timetable_data,
                "employees": employee_data
            }
            timetables_data[date_str].append(response_data)

        return jsonify(timetables_data), 200
    except Exception as e:
        return jsonify({"error" : str(e)})

def update_timetable_employee_info(time_table_id, employee_id):
    try:
        employee = TimeTableEmployee.query.filter_by(time_table_id=time_table_id, id=employee_id).first()
        if employee is None:
            return jsonify({"message": "Сотрудник с таким идентификатором и/или связанным расписанием не найден"}), 404

        updated_data = request.get_json()

        if "name" in updated_data:
            employee.name = updated_data["name"]

        db.session.commit()

        return jsonify({"message": "Сотрудник успешно обновлен"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_timetable_info(tbtimetable_id):
    try:
        data = request.json

        # Найдите запись расписания по ее идентификатору
        timetable = TimeTable.query.get(tbtimetable_id)
        if timetable is None:
            return jsonify({"message": "Расписание с таким идентификатором не найдено"}), 404

        # Обновите данные расписания
        timetable.update(data.get('timetable_data'))

        # Обновите данные связанного сотрудника
        employee = TimeTableEmployee.query.filter_by(time_table_id=tbtimetable_id).first()
        if employee:
            employee.update(data.get('employee_data'))

        return jsonify({"message": "Записи в таблицах успешно обновлены"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def create_timetable_info():
    try:
        data = request.json

        # Создайте запись в таблице расписания
        new_timetable = TimeTable.create(data.get('timetable_data'))

        # Создайте запись о сотруднике и свяжите его с созданным расписанием
        employee_data = data.get('employee_data')
        employee_data['time_table_id'] = new_timetable.tbtimetable_id
        TimeTableEmployee.create(employee_data)

        return jsonify({"message": "Записи в таблицах успешно созданы", "timetable_id": new_timetable.tbtimetable_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



def delete_timetable_info(tbtimetable_id):
    try:
        timetable = TimeTable.query.get(tbtimetable_id)
        if timetable is None:
            return jsonify({"message": "Строка в таблице расписания не найдена"}), 404
        db.session.query(TimeTableEmployee).filter(TimeTableEmployee.time_table_id == tbtimetable_id).delete()
        timetable.delete()
        return jsonify({"message": "Строка в таблице расписания успешно удалена"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_timetable_employee_info():
    try:
        data = request.json  
        new_employee = TimeTableEmployee.create(data)
        return jsonify({"message": "Сотрудник был успешно добавлен ", "id": new_employee.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_timetable_employee_info(id):
    try:
        employee = TimeTableEmployee.query.get(id)
        if employee is None:
            return jsonify({"message": "Сотрудник не был найден"}), 404
        employee.delete()
        return jsonify({"message": "Сотрудник был успешно удален из этого расписания"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
