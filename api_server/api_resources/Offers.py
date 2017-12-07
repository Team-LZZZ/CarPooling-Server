from flask import request, jsonify, g
from flask_restful import Resource
from .GetToken import auth
from api_server import db
from ..database import Offer, Location, User, Car, Reservation
from sqlalchemy import desc


class Offers(Resource):
    """
    this is the api for the offers resource
    """
    decorators = [auth.login_required]

    def encode_json(offers, clients):
        result = []
        for i in range(0, len(offers)):
            unit = {}
            unit['start_zip'] = offers[i][0]
            unit['start_st'] = offers[i][1]
            unit['start_stnum'] = offers[i][2]
            unit['end_zip'] = offers[i][3]
            unit['end_st'] = offers[i][4]
            unit['end_stnum'] = offers[i][5]
            unit['start_city'] = offers[i][6]
            unit['end_city'] = offers[i][7]
            unit['time'] = offers[i][8]
            unit['available'] = offers[i][9]
            unit['oid'] = offers[i][10]
            unit['clients'] = clients[i]
            result.append(unit)
        return result

    def get(self):
        # get current offers.
        start = db.aliased(Location)
        end = db.aliased(Location)
        allCarPools = db.session.query(start.zip, start.street, start.street_num,
                                       end.zip, end.street, end.street_num, start.city, end.city, Offer.time,
                                       Offer.seats_available, Offer.oid). \
            filter(start.longitude == Offer.start_longitude, start.latitude == Offer.start_latitude,
                   end.longitude == Offer.end_longitude, end.latitude == Offer.end_latitude,
                   g.user.id == Offer.offer_id). \
            order_by(desc(Offer.oid)).all()
        clients = db.session.query(Reservation.num, User.name, User.email, User.phone). \
            filter(g.user.id == Offer.offer_id, Offer.oid == Reservation.o_id,
                   Reservation.client_id == User.id).group_by(Reservation.o_id). \
            order_by(desc(Offer.oid)).all()
        print(clients)

        result = {}
        offerer = {}
        offerer['name'] = "zy"
        offerer['phone'] = "456788"
        offerer['email'] = "e@w.com"
        start = {}
        start['streetNumber'] = "32"
        start['street'] = "john"
        start['city'] = "wor"
        start['state'] = "MA"
        start['zip'] = "32567"
        result['startLocation'] = start
        result['targetLocation'] = start
        list = []
        list.append(offerer)
        list.append(offerer)
        result['reserverList'] = list
        result['date'] = '1970-01-01'
        result['time'] = '00:00:00'
        result['oid'] = 1
        result['available'] = 5
        re = {}
        re['status'] = True
        re['message'] = result
        return jsonify(re)

        # return jsonify(Offers.encode_json(allCarPools, clients))


def post(self):
    # create new offers.
    # form = CurrencySearchForm.from_json(request.get_json())
    # if form.validate_on_submit():
    #     search_currency_post = Post.query.filter_by(c1_item=form.c1_item.data, c2_item=form.c2_item.data,
    #                                                 league=form.league.data)
    #     search_currency_post = search_currency_post.order_by(Post.time)
    #     return jsonify([n.as_dict() for n in search_currency_post])
    # return jsonify({"post_search_status": False, "message": form.errors})
    return jsonify({"status": True})


def delete(self):
    # delete offers.
    return
