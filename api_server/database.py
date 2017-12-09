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
    password_hash = db.Column(db.String(128))
    offers = db.relationship('Offer', backref='user')
    reservations = db.relationship('Reservation', backref='user')

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
    id = db.Column(db.Integer, primary_key=True)
    oid = db.Column(db.Integer, db.ForeignKey('Offer.id'))
    longitude = db.Column(db.Float(64))
    latitude = db.Column(db.Float(64))
    street_num = db.Column(db.Integer)
    street = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    zip = db.Column(db.String(64))

    def __repr__(self):
        return '<Location %r>' % self.id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Reservation(db.Model):
    __tablename__ = 'Reservation'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    oid = db.Column(db.Integer, db.ForeignKey('Offer.id'))
    num = db.Column(db.Integer)

    def __repr__(self):
        return '<Reservation %r>' % self.id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Offer(db.Model):
    __tablename__ = 'Offer'
    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    time = db.Column(db.BigInteger)
    seats_available = db.Column(db.Integer)
    reservations = db.relationship('Reservation', backref='offer')
    car = db.relationship('Car', backref='offer', uselist=False)
    start_location = db.relationship('Location', backref='offer_s', uselist=False)
    end_location = db.relationship('Location', backref='offer_e', uselist=False)

    # db.ForeignKeyConstraint(['start_longitude', 'start_latitude'], ['Location.latitude', 'Location.longitude'])
    # db.ForeignKeyConstraint(['end_longitude', 'end_latitude'], ['Location.latitude', 'Location.longitude'])

    def __repr__(self):
        return '<Offer %r>' % self.id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Car(db.Model):
    __tablename__ = 'Car'
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(64))
    make = db.Column(db.String(32))
    model = db.Column(db.String(32))
    oid = db.Column(db.Integer, db.ForeignKey('Offer.id'))

    def __repr__(self):
        return '<Car %r>' % self.id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
