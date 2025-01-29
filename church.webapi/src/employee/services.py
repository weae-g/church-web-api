from .models import Employee, EmployeeImage
from .serialize import EmployeeSchema
from flask import request, jsonify, send_file
from io import BytesIO
import os
from create_app import db
from datetime import datetime
from urllib.parse import quote
EmployeeSchemas = EmployeeSchema(many=True)
EmployeeSchemasOne = EmployeeSchema(many=False)


def get_employee_image(employee_image_id):
    try:
        employee_image = EmployeeImage.query.get(employee_image_id)

        if not employee_image:
            return jsonify({"message": "Изображение не найдено"}), 404

        if not employee_image.image:
            return jsonify({"message": "Изображение отсутствует"}), 404

        mime_type = 'image/jpeg'  

        return send_file(BytesIO(employee_image.image), mimetype=mime_type)
    except Exception as e:
        return jsonify({"Ошибка": str(e)}), 500

def search_employee():       
    decoded_search_name = request.form['search_text']

    employees_with_name = db.session.query(Employee).filter(Employee.employee_name.ilike(f"%{decoded_search_name}%")).first()

    if employees_with_name is None:
        return jsonify({"message": "Не найдено вхождений"}), 500

    result = EmployeeSchemasOne.dump(employees_with_name)
    return jsonify(result), 200

def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    result = EmployeeSchemasOne.dump(employee) 
    return jsonify(result), 200


def get_employees():    
    employees = Employee.query.all()
    result = EmployeeSchemas.dump(employees)
    return jsonify(result)


def update_employee(employee_id):    
    try:
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({"error": "Сотрудник не найден"}), 404

        data = request.form
        
        employee.employee_name = data.get('employee_name', employee.employee_name)
        employee.employee_email = data.get('employee_email', employee.employee_email)
        employee.employee_phone = data.get('employee_phone', employee.employee_phone)
        employee.employee_description_about = data.get('employee_description_about', employee.employee_description_about)
        
        if 'employee_date' in data:
            date_string = data['employee_date']
            date_format = "%d.%m.%Y"
            employee_date = datetime.strptime(date_string, date_format)
            employee.employee_date = employee_date
            
        db.session.commit()

        return jsonify({"message": "Данные сотрудника успешно обновлены"})
    except Exception as e:
        return jsonify({"error": str(e)})


def delete_employee(employee_id):
    try:
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({"error": "Сотрудник не найден"}), 404

        EmployeeImage.query.filter_by(employee_id=employee_id).delete()

        db.session.delete(employee)
        db.session.commit()

        return jsonify({"message": "Сотрудник и его изображения успешно удалены"})
    except Exception as e:
        return jsonify({"error": str(e)})


def create_employee():
    try:
        data = request.form
        date_string = data.get('employee_date')
        date_format = "%d.%m.%Y"
        employee_date = datetime.strptime(date_string, date_format)
        new_employee = Employee(
            employee_name=data.get('employee_name'),
            employee_email=data.get('employee_email'),
            employee_date=employee_date,
            employee_phone=data.get('employee_phone'),
            employee_description_about=data.get('employee_description_about')
        )

        db.session.add(new_employee)
 

        for file in request.files.getlist('employee_images'):
            if file:
                image_data = file.read() 


                new_image = EmployeeImage(
                    image=image_data,
                    employee=new_employee
                )

                db.session.add(new_image)
        db.session.commit()

        return jsonify({"message": "Сотрудник и изображения успешно созданы"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})


def create_employee_image():
    try:
        if 'image' not in request.files:
            return jsonify({"message": "Изображение отсутствует в запросе"}), 400

        employee_id = request.form.get('employee_id')

        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"message": "Сотрудник не найден"}), 404

        image = request.files['image'].read()

        EmployeeImage.query.filter_by(employee=employee).delete()

        new_image = EmployeeImage(
            image=image,
            employee=employee
        )

        db.session.add(new_image)
        db.session.commit()

        return jsonify({"message": "Изображение успешно создано для сотрудника", "image_id": new_image.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"Ошибка": str(e)}), 500



def delete_employee_image(image_id):   
    try:

        image = EmployeeImage.query.get(image_id)

        if not image:
            return jsonify({"error": "Изображение не найдено"}), 404

        db.session.delete(image)
        db.session.commit()

        return jsonify({"message": "Изображение успешно удалено"})
    except Exception as e:
        return jsonify({"error": str(e)})