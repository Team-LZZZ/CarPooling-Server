from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange, Optional
from .database import User


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    phone = StringField('Phone')
    photo = StringField('Photo')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValueError('Username already used')


class UpdateForm(FlaskForm):
    name = StringField('Name')
    phone = IntegerField('Phone')
    new_password = PasswordField('New Password')
    photo = StringField('Photo')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValueError('Username already used')

            # def validate_current_password(self, field):
            #     temp = User.query.filter_by(id=g.user.id).first()
            #     if not temp.verify_password(field.data):
            #         raise ValueError('Wrong Password')


# class OfferForm(FlaskForm):
#     start_longitude = FloatField('start_longitude', validators=[DataRequired()])
#     start_latitude = FloatField('start_latitude', validators=[DataRequired()])
#     target_longitude = FloatField('target_longitude', validators=[DataRequired()])
#     target_latitude = FloatField('target_latitude', validators=[DataRequired()])
#     time = IntegerField('time', validators=[DataRequired()])
#     seats_available = IntegerField('seatsAvailable', validators=[DataRequired()])
#     plate = StringField('plate', validators=[DataRequired(), Length(1, 64)])
#     make = StringField('make', validators=[DataRequired(), Length(1, 32)])
#     model = StringField('model', validators=[DataRequired(), Length(1, 32)])
#     start_address = StringField('start_address', validators=[DataRequired(), Length(1, 128)])
#     target_address = StringField('target_address', validators=[DataRequired(), Length(1, 128)])


class ReservationForm(FlaskForm):
    offer_id = IntegerField('offer_id', validators=[DataRequired()])
    num = IntegerField('num', default=1)


class CarPoolSearchForm(FlaskForm):
    time = IntegerField('time')
    target_longitude = FloatField('target_longitude', validators=[DataRequired()])
    target_latitude = FloatField('target_latitude', validators=[DataRequired()])
