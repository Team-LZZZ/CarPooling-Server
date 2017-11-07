from flask import jsonify
from flask_restful import Resource
from ..database import CarPools, Location
from api_server import db


class ListAllCarPools(Resource):
    # get allCarPools.
    def get(self):
        start = db.aliased(Location)
        end = db.aliased(Location)
        allCarPools = db.session.query(start.zip, start.street, start.streetNum,
                                       end.zip, end.street, end.streetNum, CarPools.time). \
            filter(start.ll == CarPools.startLocationLL, end.ll == CarPools.targetLocationLL).all()
        return jsonify(allCarPools)
