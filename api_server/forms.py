from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField, FloatField, FieldList, FormField, \
    DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
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
    phone = StringField('Phone', default=0)

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValueError('Email already used')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValueError('Username already used')


class UpdateForm(FlaskForm):
    email = StringField('Email')
    phone = IntegerField('Phone')
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password')

    def validate_current_password(self, field):
        temp = User.query.filter_by(id=g.user.id).first()
        if not temp.verify_password(field.data):
            raise ValueError('Wrong Password')


class OfferForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    start_longitude = FloatField('start_longitude', validators=[DataRequired()])
    start_latitude = FloatField('start_latitude', validators=[DataRequired()])
    target_longitude = FloatField('target_longitude', validators=[DataRequired()])
    target_latitude = FloatField('target_latitude', validators=[DataRequired()])
    time = DateTimeField('time', validators=[DataRequired()])
    seats_available = IntegerField('seatsAvailable', validators=[DataRequired()])
    car_plate = StringField('carPlate', validators=[DataRequired(), Length(1, 64)])


class ReservationForm(FlaskForm):
    offer_name = StringField('Offer', validators=[DataRequired(), Length(1, 64)])
    client_name = StringField('Client', validators=[DataRequired(), Length(1, 64)])
    time = DateTimeField('time', validators=[DataRequired()])
    num = IntegerField('num', default=1)


class CarPoolSearchForm(FlaskForm):
    time = DateTimeField('time')
    target_longitude = FloatField('target_longitude', validators=[DataRequired()])
    target_latitude = FloatField('target_latitude', validators=[DataRequired()])
