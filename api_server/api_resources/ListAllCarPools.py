from flask import jsonify, g
from flask_restful import Resource
from ..database import CarPools, Location
from api_server import db


class ListAllCarPools(Resource):
    # get allCarPools.
    def get(self):
        allCarPools = db.session.query(Location.zip, Location.street, Location.streetNum, CarPools.time). \
            filter(Location.ll == CarPools.startLocationLL).all()
        return jsonify([n.as_dict() for n in allCarPools])
