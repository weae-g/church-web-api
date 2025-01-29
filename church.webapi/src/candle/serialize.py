from marshmallow import Schema, fields

class CandlePrayerSchema(Schema):
    class Meta:
        fields = ("id", "name")

class CandelIconSchema(Schema):
    class Meta:
        fields = ("id", "name")

class CandleTypeSchema(Schema):
    class Meta:
        fields = ("id", "name", "cost")

class CandleSchema(Schema):
    candle_type = fields.Nested(CandleTypeSchema)
    candle_icon = fields.Nested(CandelIconSchema)
    candle_prayer = fields.Nested(CandlePrayerSchema)

    class Meta:
        fields = ("tbpayment_candel_id", "cost", "day", "to_name", "author", "phone_number", "candle_type", "candle_icon", "candle_prayer")
