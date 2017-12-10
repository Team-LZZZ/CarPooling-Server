from flask import request, jsonify
from flask_restful import Resource
from ..forms import RegistrationForm
from ..database import User
from api_server import db


class UserRegister(Resource):
    """
        this is the API for user registration
    """

    def post(self):
        """
        register_form is what we get to insert into the database
        register_form should has the following value
        name, email, password
        """

        form = RegistrationForm.from_json(request.get_json())
        if form.validate_on_submit():
            new_user = User(name=form.name.data, password=form.password.data, phone=form.phone.data,
                            email=form.email.data, photo=form.photo.data)
            db.session.add(new_user)
            return jsonify({"status": True})
        error_message = [form.errors[n] for n in form.errors][0]
        return jsonify({"status": False, "message": error_message})
