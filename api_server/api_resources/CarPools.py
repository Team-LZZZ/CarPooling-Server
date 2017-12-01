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

    def get(self):
        # get allCarPools.
        start = db.aliased(Location)
        end = db.aliased(Location)
        allCarPools = db.session.query(start.zip, start.street, start.street_num,
                                       end.zip, end.street, end.street_num, Offer.time). \
            filter(start.ll == Offer.start_location, end.ll == Offer.target_location). \
            order_by(desc(Offer.time)).all()

        return jsonify(allCarPools)

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

        return jsonify(carPools)
