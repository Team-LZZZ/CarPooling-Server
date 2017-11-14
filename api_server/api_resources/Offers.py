from flask import request, jsonify
from flask_restful import Resource
from .GetToken import auth


class Offers(Resource):
    """
    this is the api for the offers resource
    """
    decorators = [auth.login_required]

    def get(self):
        # get current offers.
        return

    def post(self):
        # create new offers.
        form = CurrencySearchForm.from_json(request.get_json())
        if form.validate_on_submit():
            search_currency_post = Post.query.filter_by(c1_item=form.c1_item.data, c2_item=form.c2_item.data,
                                                        league=form.league.data)
            search_currency_post = search_currency_post.order_by(Post.time)
            return jsonify([n.as_dict() for n in search_currency_post])
        return jsonify({"post_search_status": False, "message": form.errors})

    def delete(self):
        # delete offers.
        return
