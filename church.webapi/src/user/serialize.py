from marshmallow import Schema, fields

class TbuserSchema(Schema):
    id = fields.UUID()
    login = fields.String()
    password = fields.String()

class UserRolesSchema(Schema):
    role_id = fields.UUID()
    role = fields.String()

class UsersSchema(Schema):
    id = fields.UUID()
    user_id = fields.UUID()
    role_id = fields.UUID()
    tbuser = fields.Nested(TbuserSchema)
    user_roles = fields.Nested(UserRolesSchema, many=True)
