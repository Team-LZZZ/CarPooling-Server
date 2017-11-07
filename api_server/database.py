from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from config import TestConfig

app = Flask(__name__)
app.config.from_object(TestConfig)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.Integer)
    photo = db.Column(db.String(64))
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def generate_auth_token(self, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Location(db.Model):
    __tablename__ = 'Location'
    ll = db.Column(db.String(128), primary_key=True)
    streetNum = db.Column(db.Integer)
    street = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip = db.Column(db.Integer)


    # def __repr__(self):
    #     return '<Search %r>' % self.sid
    #
    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CarPools(db.Model):
    __tablename__ = 'CarPools'
    offerId = db.Column(db.Integer, db.ForeignKey('User.id'))
    clientId = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    startLocationLL = db.Column(db.String(128), db.ForeignKey('Location.ll'))
    targetLocationLL = db.Column(db.String(128), db.ForeignKey('Location.ll'))
    carPlate = db.Column(db.String(64), db.ForeignKey('Car.plate'))
    time = db.Column(db.DateTime, primary_key=True)

    # def __repr__(self):
    #     return '<Post %r>' % self.tid
    #
    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Car(db.Model):
    __tablename__ = 'Car'
    plate = db.Column(db.String(64), primary_key=True)
    make = db.Column(db.String(64))
    model = db.Column(db.String(64))
    seatsLimit = db.Column(db.Integer)

    # def __repr__(self):
    #     return '<Currency %r>' % self.cid
    #
    # def as_dict(self):
    #     return {c.name: getattr(self, c.name) for c in self.__table__.columns}
