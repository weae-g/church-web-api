from marshmallow import Schema, fields

class PaymentNoteNameSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'cost', 'id_type')
        
class PaymentNoteTypeSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'cost', 'payment_note_names')
    
    payment_note_names = fields.Nested(PaymentNoteNameSchema, many=True)

class PaymentInfoSchema(Schema):
    class Meta:
        fields = ('id', 'payment_id', 'amount', 'currency', 'status', 'created_at', 'updated_at', 'user_email',
                  'from_name', 'user_name', 'phone_number', 'note_cost', 'note_name', 'note_type', 'donation', 
                  'type', 'email_sent', 'email_sent_et2', 'candle_type', 'candle_icon', 'candle_payer', 'day')


class PaymentNoteSchema(Schema):
    class Meta:
        fields = ( 'tbpayment_note_id', 'tbpayment_note_type_id', 'tbpayment_note_name_id', 'author',
                   'phone_number', 'to_name', 'at_work', 'finish',  'payment_info')

    payment_note_type = fields.Nested(PaymentNoteTypeSchema, many=False)
    payment_note_name = fields.Nested(PaymentNoteNameSchema, many=False)
    payment_info = fields.Nested(PaymentInfoSchema, many=False)

