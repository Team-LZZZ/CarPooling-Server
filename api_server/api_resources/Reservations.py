from flask import request, jsonify, g
from flask_restful import Resource
from api_server import db
import datetime
import sys
from .GetToken import auth


class Reservations(Resource):
    """
        this is the API for reservations resource
    """
    decorators = [auth.login_required]

    def get(self):
        # get current reservations.
        return

    def post(self, tid=None):
        # create new reservations.
        if tid:
            return jsonify({"new_post_status": False, "message": "Wrong usage"})

        if not g.user:
            return jsonify({"login_staus": False, "message": "Please login"})

        form = PostTradeForm.from_json(request.get_json())
        if form.validate_on_submit():
            post = Post(uid=g.user.id, c1_item=form.c1_item.data, c2_item=form.c2_item.data,
                        c1_number=form.c1_number.data, c2_number=form.c2_number.data, league=form.league.data,
                        name=form.user_name.data, time=datetime.datetime.now())
            db.session.add(post)
            db.session.commit()
            return jsonify({"post_status": True})
        return jsonify({"post_status": False, "message": form.errors})

    def delete(self, tid):
        # delete reservations.
        try:
            trade = Post.query.filter_by(tid=tid).first()
            if trade and trade.uid == g.user.id:
                db.session.delete(trade)
                db.session.commit()
            return jsonify({"delete_post_status": "Success"})
        except:
            return jsonify({"delete_post_status": False, "message": sys.exc_info()[0]})
