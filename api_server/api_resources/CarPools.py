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
            unit = {}
            unit['start_zip'] = i[0]
            unit['start_st'] = i[1]
            unit['start_stnum'] = i[2]
            unit['end_zip'] = i[3]
            unit['end_st'] = i[4]
            unit['end_stnum'] = i[5]
            unit['start_city'] = i[6]
            unit['end_city'] = i[7]
            unit['time'] = i[8]
            unit['available'] = i[9]
            unit['name'] = i[10]
            unit['email'] = i[11]
            unit['phone'] = i[12]
            unit['oid'] = i[13]
            unit['plate'] = i[14]
            unit['make'] = i[15]
            unit['model'] = i[16]
            result.append(unit)
        re = {}
        re['status'] = True
        re['message'] = result
        return jsonify(re)

    def get(self):
        # get allCarPools.
        start = db.aliased(Location)
        end = db.aliased(Location)
        allCarPools = db.session.query(start.zip, start.street, start.street_num,
                                       end.zip, end.street, end.street_num, start.city, end.city, Offer.time,
                                       Offer.seats_available, User.name, User.email, User.phone, Offer.oid, Car.plate,
                                       Car.make, Car.model). \
            filter(start.longitude == Offer.start_longitude, start.latitude == Offer.start_latitude,
                   end.longitude == Offer.end_longitude, end.latitude == Offer.end_latitude, User.id == Offer.offer_id,
                   Car.plate == Offer.car_plate). \
            order_by(desc(Offer.time)).all()

        result = {}
        car = {}
        car['plate'] = "65dfl"
        car['model'] = "mazda 6"
        car['make'] = "mazda"
        result['car'] = car
        offerer = {}
        offerer['name'] = "zy"
        offerer['phone'] = "456788"
        offerer['email'] = "e@w.com"
        result['offerer'] = offerer
        start = {}
        start['streetNumber'] = "32"
        start['street'] = "john"
        start['city'] = "wor"
        start['state'] = "MA"
        start['zip'] = "32567"
        result['startLocation'] = start
        result['targetLocation'] = start
        result['date'] = '1970-01-01'
        result['time'] = '00:00:00'
        result['oid'] = 1
        result['available'] = 5
        list = []
        list.append(str(result))
        re = {}
        re['status'] = True
        re['message'] = list
        return jsonify(re)
        # return jsonify(CarPools.encode_json(allCarPools))

    def post(self):
        # query CarPools.
        start = db.aliased(Location)
        end = db.aliased(Location)
        form = CarPoolSearchForm.from_json(request.get_json())
        if form.time.data:
            carPools = db.session.query(start.zip, start.street, start.street_num,
                                        end.zip, end.street, end.street_num, start.city, end.city, Offer.time,
                                        Offer.seats_available, User.name, User.email, User.phone, Offer.oid, Car.plate,
                                        Car.make, Car.model). \
                filter(start.longitude == Offer.start_longitude, start.latitude == Offer.start_latitude,
                       end.longitude == Offer.end_longitude, end.latitude == Offer.end_latitude,
                       User.id == Offer.offer_id, Car.plate == Offer.car_plate,
                       end.longitude == form.target_longitude.data, end.latitude == form.target_latitude.data,
                       Offer.time == form.time.data). \
                order_by(desc(Offer.time)).all()
        else:
            carPools = db.session.query(start.zip, start.street, start.street_num,
                                        end.zip, end.street, end.street_num, start.city, end.city, Offer.time,
                                        Offer.seats_available, User.name, User.email, User.phone, Offer.oid, Car.plate,
                                        Car.make, Car.model). \
                filter(start.longitude == Offer.start_longitude, start.latitude == Offer.start_latitude,
                       end.longitude == Offer.end_longitude, end.latitude == Offer.end_latitude,
                       User.id == Offer.offer_id, Car.plate == Offer.car_plate,
                       end.longitude == form.target_longitude.data, end.latitude == form.target_latitude.data). \
                order_by(desc(Offer.time)).all()

        result = {}
        car = {}
        car['plate'] = "65dfl"
        car['model'] = "mazda 6"
        car['make'] = "mazda"
        result['car'] = car
        offerer = {}
        offerer['name'] = "zy"
        offerer['phone'] = "456788"
        offerer['email'] = "e@w.com"
        result['offerer'] = offerer
        start = {}
        start['streetNumber'] = "32"
        start['street'] = "john"
        start['city'] = "wor"
        start['state'] = "MA"
        start['zip'] = "32567"
        result['startLocation'] = start
        result['targetLocation'] = start
        result['date'] = '1970-01-01'
        result['time'] = '00:00:00'
        result['oid'] = 1
        result['available'] = 5
        list = []
        list.append(str(result))
        re = {}
        re['status'] = True
        re['message'] = list
        print(list)
        return jsonify(re)

        # return jsonify(CarPools.encode_json(carPools))
