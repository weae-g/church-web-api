from marshmallow import Schema, fields

class BrickSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    message = fields.Str()
    cost = fields.Decimal(as_string=True)
    color = fields.Str()
    date = fields.Date()
    mail = fields.Str()

    class Meta:
        fields = ("id", "name", "message", "cost", "color", "date", "mail")

class BrickSchemaCreate(Schema):
    id = fields.UUID()
    name = fields.Str()
    message = fields.Str()
    cost = fields.Decimal(as_string=True)
    color = fields.Str()
    mail = fields.Str()

    class Meta:
        fields = ("id", "name", "message", "cost", "color", "mail")
