from flask import jsonify, request
from flask_restful import Resource
from ..database import CarPool, Location
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
        allCarPools = db.session.query(start.zip, start.street, start.streetNum,
                                       end.zip, end.street, end.streetNum, CarPool.time). \
            filter(start.ll == CarPool.startLocationLL, end.ll == CarPool.targetLocationLL). \
            order_by(desc(CarPool.time)).all()

        return jsonify(allCarPools)

    def post(self):
        # query CarPools.
        start = db.aliased(Location)
        end = db.aliased(Location)
        # query = []
        form = CarPoolSearchForm.from_json(request.get_json())
        carPools = db.session.query(start.zip, start.street, start.streetNum,
                                    end.zip, end.street, end.streetNum, CarPool.time). \
            filter(start.ll == CarPool.startLocationLL, end.ll == CarPool.targetLocationLL,
                   start.ll == form.start.data, end.ll == form.end.data). \
            order_by(desc(CarPool.time)).all()

        return jsonify(carPools)
