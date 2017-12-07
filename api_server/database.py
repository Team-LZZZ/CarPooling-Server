from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from config import DevelopmentConfig
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(64))
    password = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    offers = db.relationship('Offer', backref='user')
    reservations = db.relationship('Reservation', backref='reservation_u')

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
    longitude = db.Column(db.Float(32), primary_key=True)
    latitude = db.Column(db.Float(32), primary_key=True)
    street_num = db.Column(db.Integer)
    street = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip = db.Column(db.String(64))

    def __repr__(self):
        return '<Location %r>' % self.longitude, self.latitude

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Reservation(db.Model):
    __tablename__ = 'Reservation'
    rid = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    o_id = db.Column(db.Integer, db.ForeignKey("Offer.oid"))
    num = db.Column(db.Integer)

    def __repr__(self):
        return '<Reservation %r>' % self.rid

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Offer(db.Model):
    __tablename__ = 'Offer'
    oid = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    time = db.Column(db.DateTime)
    start_longitude = db.Column(db.Float(32))
    start_latitude = db.Column(db.Float(32))
    end_longitude = db.Column(db.Float(32))
    end_latitude = db.Column(db.Float(32))
    car_plate = db.Column(db.String(64), db.ForeignKey('Car.plate'))
    seats_available = db.Column(db.Integer)
    reservations = db.relationship('Reservation', backref='reservation_o')
    db.ForeignKeyConstraint(['start_longitude', 'start_latitude'], ['Location.latitude', 'Location.longitude'])
    db.ForeignKeyConstraint(['end_longitude', 'end_latitude'], ['Location.latitude', 'Location.longitude'])

    def __repr__(self):
        return '<Offer %r>' % self.oid

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Car(db.Model):
    __tablename__ = 'Car'
    plate = db.Column(db.String(64), primary_key=True)
    make = db.Column(db.String(32))
    model = db.Column(db.String(32))

    def __repr__(self):
        return '<Car %r>' % self.plate

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
