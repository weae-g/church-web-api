from marshmallow import Schema, fields

class PaymentNoteNameSchema(Schema):
    class Meta:
        fields = ('id', 'name')
        
class PaymentNoteTypeSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'cost', 'payment_note_names')
    
    payment_note_names = fields.Nested(PaymentNoteNameSchema, many=True)

class PaymentNoteSchema(Schema):
    class Meta:
        fields = ('tbpayment_note_id','tbpayment_note_id',  'author', 'phone_number', 'to_name',  'payment_note_name')
    
    payment_note_type = fields.Nested(PaymentNoteTypeSchema, many=False)
    payment_note_name = fields.Nested(PaymentNoteNameSchema, many=False)
