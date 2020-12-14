import os
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy import Float, DateTime, relationship, ForeignKey
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
    status = Column(String(20))
    reserves = relationship('Reserve', backref='clothes', lazy=True)

    def __init__(self, type, size):
        self.type = type
        self.size = size

    def insert(self):
        self.registered_time = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.registered_time = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
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
    e_mail = Column(String(120), nullable=False, unique=True)
    address = Column(String(500))
    reserves = relationship('Reserve', backref='user', lazy=True)

    def __init__(self, e_mail, address=""):
        self.e_mail = e_mail
        self.address = address
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def rollback(self):
        db.session.rollback()
    
    def close_session(self):
        db.session.close()

    def format(self):
        return {
            'id': self.id,
            'e_mail': self.e_mail,
            'address': self.address
        }

# --------------------------------------------- #
# Reserves
# Relational table between clothes and users
# --------------------------------------------- #
class Reserve(db.Model):  
    __tablename__ = 'reserves'

    id = Column(Integer, primary_key=True)
    clothes_id = Column(Integer, ForeignKey('clothes.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
