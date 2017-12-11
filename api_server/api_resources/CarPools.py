from flask import jsonify, request
from flask_restful import Resource
from ..database import Offer, Location, User, Car
from api_server import db
from api_server.forms import CarPoolSearchForm
from sqlalchemy import desc
from .GetToken import auth
import time


class CarPools(Resource):
    """
        this is the API for carpools resource
    
    """
    decorators = [auth.login_required]

    def encode_json(carpools):
        result = []
        for i in carpools:
            start = {}
            end = {}
            car = {}
            offerer = {}
            start['address'] = i.locations[0].address
            end['address'] = i.locations[1].address
            offerer['name'] = i.user.name
            offerer['email'] = i.user.email
            offerer['phone'] = i.user.phone
            offerer['photo'] = i.user.photo
            car['make'] = i.car.make
            car['model'] = i.car.model
            car['plate'] = i.car.plate
            start['longitude'] = i.locations[0].longitude
            end['longitude'] = i.locations[1].longitude
            start['latitude'] = i.locations[0].latitude
            end['latitude'] = i.locations[1].latitude

            element = {}
            element['time'] = i.time
            element['available'] = i.seats_available
            element['oid'] = i.id
            element['car'] = car
            element['offerer'] = offerer
            element['startLocation'] = start
            element['targetLocation'] = end
            result.append(str(element))
        re = {}
        re['status'] = True
        re['message'] = result
        return re

    def get(self):
        # get allCarPools.
        # start = db.aliased(Location)
        # end = db.aliased(Location)
        # allCarPools = db.session.query(start.zip, start.street, start.street_num,
        #                                end.zip, end.street, end.street_num, start.city, end.city, Offer.time,
        #                                Offer.seats_available, User.name, User.email, User.phone, Offer.oid, Car.plate,
        #                                Car.make, Car.model, start.state, end.state). \
        #     filter(start.longitude == Offer.start_longitude, start.latitude == Offer.start_latitude,
        #            end.longitude == Offer.end_longitude, end.latitude == Offer.end_latitude, User.id == Offer.offer_id,
        #            Car.plate == Offer.car_plate). \
        #     order_by(desc(Offer.time)).all()
        t = time.time()
        offers = Offer.query.filter(Offer.time >= int(round(t * 1000))).order_by(desc(Offer.time)).all()
        return jsonify(CarPools.encode_json(offers))

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
        # result['date'] = '1970-01-01'
        # result['time'] = '00:00:00'
        # result['oid'] = 1
        # result['available'] = 5
        # list = []
        # list.append(str(result))
        # re = {}
        # re['status'] = True
        # re['message'] = list
        # return jsonify(re)

    def post(self):
        # query CarPools.
        t = time.time()
        form = CarPoolSearchForm.from_json(request.get_json())
        if form.time.data:
            offers = Offer.query.join(Offer.locations).filter(Offer.time == form.time.data,
                                                              Offer.time >= int(round(t * 1000)),
                                                              Location.longitude == form.target_longitude.data,
                                                              Location.latitude == form.target_latitude.data).order_by(
                desc(Offer.time)).all()
        else:
            offers = Offer.query.join(Offer.locations).filter(Offer.time >= int(round(t * 1000)),
                                                              Location.longitude == form.target_longitude.data,
                                                              Location.latitude == form.target_latitude.data).order_by(
                desc(Offer.time)).all()

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
        # result['date'] = '1970-01-01'
        # result['time'] = '00:00:00'
        # result['oid'] = 1
        # result['available'] = 5
        # list = []
        # list.append(str(result))
        # re = {}
        # re['status'] = True
        # re['message'] = list
        # print(list)
        # return jsonify(re)
        return jsonify(CarPools.encode_json(offers))
