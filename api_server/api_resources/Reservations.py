from flask import request, jsonify, g
from flask_restful import Resource
from api_server import db
import sys
from ..database import User
from .GetToken import auth
from ..database import Offer, Location, User, Car, Reservation
from ..forms import ReservationForm


class Reservations(Resource):
    """
        this is the API for reservations resource
    """
    decorators = [auth.login_required]

    def encode_json(offers):
        result = []
        for i in offers:
            start = {}
            end = {}
            car = {}
            offerer = {}
            start['address'] = i[1].start_location.address
            end['address'] = i[1].end_location.address
            offerer['name'] = i[1].user.name
            offerer['email'] = i[1].user.email
            offerer['phone'] = i[1].user.phone
            offerer['photo'] = i[1].user.photo
            car['make'] = i[1].car.make
            car['model'] = i[1].car.model
            car['plate'] = i[1].car.plate

            list = []
            for r in i[1].reservations:
                client = {}
                client['name'] = r.user.name
                client['email'] = r.user.email
                client['phone'] = r.user.phone
                client['photo'] = r.user.photo
                list.append(client)

            element = {}
            element['time'] = i[1].time
            # element['available'] = i.seats_available
            element['rid'] = i[0]
            element['car'] = car
            element['offerer'] = offerer
            element['startLocation'] = start
            element['targetLocation'] = end
            element['reserverList'] = list
            result.append(str(element))
        re = {}
        re['status'] = True
        re['message'] = result
        return re

    def get(self):
        # get current reservations.

        current_user = User.query.filter_by(id=g.user.id).first()
        reservations = current_user.reservations
        offers = [(n.id, n.offer) for n in reservations]

        return jsonify(Reservations.encode_json(offers))
        # result = {}
        # car = {}
        # car['plate'] = "65dfl"
        # car['model'] = "mazda 6"
        # car['make'] = "mazda"
        # result['car'] = car
        # offerer = {}
        # offerer['name'] = "zy"
        # offerer['phone'] = "456788"
        # offerer['email'] = "e@w.com"
        # result['offerer'] = offerer
        # start = {}
        # start['streetNumber'] = "32"
        # start['street'] = "john"
        # start['city'] = "wor"
        # start['state'] = "MA"
        # start['zip'] = "32567"
        # result['startLocation'] = start
        # result['targetLocation'] = start
        # list = []
        # list.append(offerer)
        # list.append(offerer)
        # result['reserverList'] = list
        # result['date'] = '1970-01-01'
        # result['time'] = '00:00:00'
        # result['oid'] = 1
        # list = []
        # list.append(result)
        # re = {}
        # re['status'] = True
        # re['message'] = list
        # return jsonify(re)

    def post(self):
        # create new reservations.
        form = ReservationForm.from_json(request.get_json())
        offer = Offer.query.filter_by(id=form.offer_id.data).first()
        if form.num.data > offer.seats_available:
            error_messages = []
            error_messages.append("This offer doesn't have enough available seats your require")
            return jsonify({"status": False, "message": error_messages})
        offer.seats_available = offer.seats_available - form.num.data
        print(offer.seats_available)
        reservation = Reservation(client_id=g.user.id, num=form.num.data)
        offer.reservations.append(reservation)
        db.session.commit()
        return jsonify({"status": True})

    def delete(self):
        # delete reservations.
        rid = request.get_json()["rid"]
        reservation = Reservation.query.filter_by(id=rid).first()
        num = reservation.num
        offer = reservation.offer
        offer.seats_available = offer.seats_available + num
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({"status": True})
