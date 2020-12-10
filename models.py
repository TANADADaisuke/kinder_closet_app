import os
from sqlalchemy import Column, String, create_engine, Integer, Float, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    """binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# --------------------------------------------- #
# Clothes
# Have type, size, and registered time
# --------------------------------------------- #
class Clothes(db.Model):  
    __tablename__ = 'clothes'

    id = Column(Integer, primary_key=True)
    type = Column(String(120), nullable=False)
    size = Column(Float, nullable=False)
    registered_time = Column(DateTime, nullable=False)

    def __init__(self, type, size):
        self.type = type
        self.size = size

    def insert(self):
        self.registered_time = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def rollback(self):
        db.session.rollback()
    
    def close_session(self):
        db.session.close()

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'size': self.size,
            'registerd': self.registered_time
        }


# --------------------------------------------- #
# User
# Have e-mail and address
# --------------------------------------------- #
class User(db.Model):  
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    e_mail = Column(String(120), nullable=False)
    address = Column(String(500))

    def __init__(self, e_mail, address=""):
        self.e_mail = e_mail
        self.address = address

    def format(self):
        return {
            'id': self.id,
            'e_mail': self.e_mail,
            'address': self.address
        }
