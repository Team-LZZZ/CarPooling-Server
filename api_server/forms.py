from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField, FloatField, FieldList, FormField, \
    DateTimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from .database import User


class LoginForm(FlaskForm):
    name = StringField('UserID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(FlaskForm):
    name = StringField('Username', validators=[Length(1, 64)])
    email = StringField('Email Address', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    phone = IntegerField('Phone', default=0)
    photo = StringField('Photo', default="")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValueError('Username already used')


class UpdateForm(FlaskForm):
    email = StringField('Email Address', validators=[Length(1, 64), Email(), Optional()])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password',
                                 validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValueError('Email already used')

    def validate_current_password(self, field):
        temp = User.query.filter_by(id=g.user.id).first()
        if not temp.verify_password(field.data):
            raise ValueError('Wrong Password')


class PostTradeForm(FlaskForm):
    user_name = StringField('Game ID', validators=[DataRequired(), Length(1, 64)])  # USER NAME IN GAME
    c1_item = StringField('Currency 1', validators=[DataRequired(), Length(1, 64)])  # The item user wants to sell
    c2_item = StringField('Currency 2', validators=[DataRequired(), Length(1, 64)])  # The item user wants to get
    c1_number = IntegerField('Currency 1 Qty', validators=[DataRequired(), NumberRange(min=1, max=999)])
    c2_number = IntegerField('Currency 2 Qty', validators=[DataRequired(), NumberRange(min=1, max=999)])
    league = StringField('League', validators=[DataRequired(), Length(1, 64)])


class UserHistoryForm(FlaskForm):
    user_id = IntegerField('User ID')
    item_name = StringField('Item', validators=[Length(1, 64)])


class CarPoolSearchForm(FlaskForm):
    time = DateTimeField('time')
    start = StringField('start', validators=[DataRequired(), Length(1, 128)])
    end = StringField('end', validators=[DataRequired(), Length(1, 128)])
