from marshmallow import Schema, fields, ValidationError

class UserRoleSchema(Schema):
    """
    Схема для сериализации и десериализации данных ролей пользователей.
    """
    role_id = fields.UUID(dump_only=True)
    role = fields.String(required=True)

class UserSchema(Schema):
    """
    Схема для сериализации и десериализации данных пользователей.
    """
    id = fields.UUID(dump_only=True)
    role_id = fields.UUID(required=True)
    login = fields.String(required=True)
    password = fields.String(required=True)

    gallery_type = fields.Nested(UserRoleSchema)

    @staticmethod
    def validate_role_id(role_id):
        # Проверяем, что role_id является UUID
        try:
            uuid.UUID(role_id)
        except ValueError:
            raise ValidationError('Invalid UUID format for role_id')

