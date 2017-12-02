from flask import jsonify, request
from flask_restful import Resource
from ..database import Offer, Location
from api_server import db
from api_server.forms import CarPoolSearchForm
from sqlalchemy import desc


class CarPools(Resource):
    """
        this is the API for carpools resource
    
    """

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
            unit['time'] = i[6]
            result.append(unit)
        return result

    def get(self):
        # get allCarPools.
        start = db.aliased(Location)
        end = db.aliased(Location)
        allCarPools = db.session.query(start.zip, start.street, start.street_num,
                                       end.zip, end.street, end.street_num, Offer.time). \
            filter(start.ll == Offer.start_location, end.ll == Offer.target_location). \
            order_by(desc(Offer.time)).all()
        return jsonify(CarPools.encode_json(allCarPools))

    def post(self):
        # query CarPools.
        start = db.aliased(Location)
        end = db.aliased(Location)
        # query = []
        form = CarPoolSearchForm.from_json(request.get_json())
        carPools = db.session.query(start.zip, start.street, start.streetNum,
                                    end.zip, end.street, end.streetNum, Offer.time). \
            filter(start.ll == Offer.start_location, end.ll == Offer.target_location,
                   start.ll == form.start_location.data, end.ll == form.target_location.data). \
            order_by(desc(Offer.time)).all()
        return jsonify(CarPools.encode_json(carPools))
