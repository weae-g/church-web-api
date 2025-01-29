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


class PaymentInfoSchema(Schema):
    class Meta:
        fields = ('id', 'payment_id', 'amount', 'currency', 'status', 'created_at', 'updated_at', 'user_email',
                  'from_name', 'user_name', 'phone_number', 'note_cost', 'note_name', 'note_type', 'donation', 
                  'type', 'email_sent', 'email_sent_et2', 'candle_type', 'candle_icon', 'candle_payer', 'day')



class CandleSchema(Schema):
    candle_type = fields.Nested(CandleTypeSchema)
    candle_icon = fields.Nested(CandelIconSchema)
    candle_prayer = fields.Nested(CandlePrayerSchema)
    payment_info = fields.Nested(PaymentInfoSchema, many=False)

    class Meta:
        fields = ("tbpayment_candel_id", "cost", "day", "to_name", "author", "phone_number", "finish" , "candle_type", "candle_icon", "candle_prayer", "payment_info")
