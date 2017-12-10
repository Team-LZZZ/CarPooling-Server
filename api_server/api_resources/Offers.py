from flask import request, jsonify, g
from flask_restful import Resource
from .GetToken import auth
from api_server import db
from ..database import Offer, Location, User, Car, Reservation
from sqlalchemy import desc
import time


class Offers(Resource):
    """
    this is the api for the offers resource
    """
    decorators = [auth.login_required]

    def encode_json(offers):
        result = []
        for i in offers:
            start = {}
            end = {}
            # car = {}
            start['address'] = i.locations[0].address
            end['address'] = i.locations[1].address
            # car['make'] = i.car.make
            # car['model'] = i.car.model
            # car['plate'] = i.car.plate

            list = []
            for r in i.reservations:
                client = {}
                client['name'] = r.user.name
                client['email'] = r.user.email
                client['phone'] = r.user.phone
                client['photo'] = r.user.photo
                client['num'] = r.num
                list.append(client)

            element = {}
            element['time'] = i.time
            element['available'] = i.seats_available
            element['oid'] = i.id
            # element['car'] = car
            element['startLocation'] = start
            element['targetLocation'] = end
            element['reserverList'] = list
            result.append(str(element))
        re = {}
        re['status'] = True
        re['message'] = result
        return re

    def get(self):
        # get current offers.
        t = time.time()
        current_user = Offer.query.filter_by(id=g.user.id).first()
        offers = current_user.offers

        # start = db.aliased(Location)
        # end = db.aliased(Location)
        # allCarPools = db.session.query(start.zip, start.street, start.street_num,
        #                                end.zip, end.street, end.street_num, start.city, end.city, Offer.time,
        #                                Offer.seats_available, Offer.oid). \
        #     filter(start.longitude == Offer.start_longitude, start.latitude == Offer.start_latitude,
        #            end.longitude == Offer.end_longitude, end.latitude == Offer.end_latitude,
        #            g.user.id == Offer.offer_id). \
        #     order_by(desc(Offer.oid)).all()
        # clients = db.session.query(Reservation.num, User.name, User.email, User.phone). \
        #     filter(g.user.id == Offer.offer_id, Offer.oid == Reservation.o_id,
        #            Reservation.client_id == User.id).group_by(Reservation.o_id). \
        #     order_by(desc(Offer.oid)).all()
        # print(clients)

        # result = {}
        # offerer = {}
        # offerer['name'] = "zy"
        # offerer['phone'] = "456788"
        # offerer['email'] = "e@w.com"
        # start = {}
        # start['address'] = "32h john st, worcester, MA, 01609"
        # result['startLocation'] = start
        # result['targetLocation'] = start
        # list = []
        # list.append(offerer)
        # list.append(offerer)
        # result['reserverList'] = list
        # result['time'] = '4555555'
        # result['oid'] = 1
        # result['available'] = 5
        # list = []
        # list.append(str(result))
        # re = {}
        # re['status'] = True
        # re['message'] = list
        # return jsonify(re)

        return jsonify(Offers.encode_json(offers))

    def post(self):
        # create new offers.
        # form = CurrencySearchForm.from_json(request.get_json())
        # if form.validate_on_submit():
        #     search_currency_post = Post.query.filter_by(c1_item=form.c1_item.data, c2_item=form.c2_item.data,
        #                                                 league=form.league.data)
        #     search_currency_post = search_currency_post.order_by(Post.time)
        #     return jsonify([n.as_dict() for n in search_currency_post])
        # return jsonify({"post_search_status": False, "message": form.errors})
        t = time.time()
        new_offer = request.get_json()
        if new_offer['time'] <= int(round(t * 1000)):
            error_messages = []
            error_messages.append("You cannot offer a carpool in the past")
            return jsonify({"status": False, "message": error_messages})
        offer = Offer(time=new_offer['time'], seats_available=new_offer['seats_available'], offer_id=g.user.id)
        car = Car(plate=new_offer['car']['plate'], make=new_offer['car']['make'], model=new_offer['car']['model'])
        start = Location(address=new_offer['startLocation']['address'],
                         longitude=new_offer['startLocation']['longitude'],
                         latitude=new_offer['startLocation']['latitude'])
        end = Location(address=new_offer['targetLocation']['address'],
                       longitude=new_offer['targetLocation']['longitude'],
                       latitude=new_offer['targetLocation']['latitude'])
        offer.car = car
        offer.locations.append(start)
        offer.locations.append(end)
        db.session.add(offer)
        return jsonify({"status": True})

    def delete(self):
        # delete offers.
        oid = request.get_json()["oid"]
        offer = Offer.query.filter_by(id=oid).first()
        db.session.delete(offer)
        return jsonify({"status": True})
