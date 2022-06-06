from aiohttp import web
from lib.settings import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    reg_time = db.Column(db.DateTime, server_default=db.func.now())
    is_authorized = db.Column(db.Boolean, unique=False, default=False)


class AdvertisementModel(db.Model):
    __tablename__ = 'advertisements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    create_time = db.Column(db.DateTime, server_default=db.func.now())
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

