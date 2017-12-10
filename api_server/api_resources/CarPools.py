from flask import jsonify, request
from flask_restful import Resource
from ..database import Offer, Location, User, Car
from api_server import db
from api_server.forms import CarPoolSearchForm
from sqlalchemy import desc
from .GetToken import auth


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
            start['address'] = i.start_location.address
            end['address'] = i.end_location.address
            offerer['name'] = i.user.name
            offerer['email'] = i.user.email
            offerer['phone'] = i.user.phone
            offerer['photo'] = i.user.photo
            car['make'] = i.car.make
            car['model'] = i.car.model
            car['plate'] = i.car.plate
            start['longitude'] = i.start_location.longitude
            end['longitude'] = i.end_location.longitude
            start['latitude'] = i.start_location.latitude
            end['latitude'] = i.end_location.latitude

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

        offers = Offer.query.all()
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
        form = CarPoolSearchForm.from_json(request.get_json())
        if form.time.data:
            offers = Offer.query.join(Offer.end_location).filter(Offer.time == form.time.data,
                                                                 Location.longitude == form.target_longitude.data,
                                                                 Location.latitude == form.target_latitude.data).all()
        else:
            offers = Offer.query.join(Offer.end_location).filter(
                Location.longitude == form.target_longitude.data,
                Location.latitude == form.target_latitude.data).all()

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
