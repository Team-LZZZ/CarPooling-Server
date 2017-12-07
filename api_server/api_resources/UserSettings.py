from flask import request, jsonify, g
from flask_restful import Resource
from ..forms import UpdateForm
from ..database import User
from api_server import db
from .GetToken import auth


class UserSettings(Resource):
    """
    this is the API for user update information
    """
    decorators = [auth.login_required]

    def put(self):
        """
        register_form is what we get to insert into the database
        register_form should has the following value
        name, email, password
        """
        form = UpdateForm.from_json(request.get_json())
        error_message = []

        if not g.user:
            error_message.append("Please login")
            return jsonify({"status": False, "message": error_message})

        if form.validate_on_submit():
            current_user = User.query.filter_by(id=g.user.id).first()
            if form.name.data:
                current_user.name = form.name.data
            if form.phone.data:
                current_user.phone = form.phone.data
            if form.new_password.data:
                current_user.password = form.new_password.data
            db.session.commit()
            return jsonify({"status": True})
        error_message = [form.errors[n] for n in form.errors][0]
        return jsonify({"status": False, "message": error_message})
