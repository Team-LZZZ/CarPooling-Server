from flask import request, jsonify
from flask_restful import Resource
from ..forms import LoginForm
from ..database import User


class UserLogin(Resource):
    """
        this is the API for user login
    """

    def post(self):
        form = LoginForm.from_json(request.get_json())
        if form.validate_on_submit():
            user = User.query.filter_by(name=form.name.data).first()
            if user and user.verify_password(form.password.data):
                token = user.generate_auth_token()
                return jsonify({"login_status": True, "token": token.decode("ascii")})
            elif not user:
                return jsonify({"login_status": False, "message": "User not exist"})
            else:
                return jsonify({"login_status": False, "message": "Wrong password"})
        else:
            return jsonify({"login_status": False, "message": form.errors})
