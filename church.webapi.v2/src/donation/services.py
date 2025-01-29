from .serialize import DonationSchema
from .models import Donation
from flask import jsonify, request
from create_app import db

donation_schema = DonationSchema()
donations_schema = DonationSchema(many=True)

def create_donation():
    data = request.json
    new_donation = Donation(**data)
    db.session.add(new_donation)
    db.session.commit()
    return jsonify(donation_schema.dump(new_donation)), 200

def get_donations():
    donations = Donation.query.all()
    return jsonify(donations_schema.dump(donations)), 200