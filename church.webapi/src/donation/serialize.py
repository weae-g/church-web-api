from marshmallow import Schema, fields

class DonationSchema(Schema):
    payment_donation_id = fields.Int(dump_only=True)
    donation_sum = fields.Decimal(as_string=True)
    donation_name = fields.Str()
    description = fields.Str()
    phone_number = fields.Str()
    mail = fields.Str()
