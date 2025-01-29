from marshmallow import Schema, fields
import base64
class EmployeeRoleSchema(Schema):
    class Meta:
        fields = ("id", "name", "employee_id")

class EmployeeImageSchema(Schema):
    class Meta:
        fields = ("id", "employee_id", "image")

    image = fields.Method("get_image_url")

    def get_image_url(self, obj):
        if obj.image is not None:
            return f"/api/employee_image/{obj.id}"  
        else:
            return None


class EmployeeSchema(Schema):
    employee_id = fields.UUID()
    employee_name = fields.String()
    employee_email = fields.String()
    employee_phone = fields.String()
    employee_description_about = fields.String()
    employee_date = fields.DateTime()

    employee_role = fields.Nested(EmployeeRoleSchema, many=True)
    employee_image = fields.Nested(EmployeeImageSchema, many=True)
        
