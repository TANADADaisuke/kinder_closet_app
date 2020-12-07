import os
from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()
    return db


'''
Person
Have title and release year
'''
class Person(db.Model):  
  __tablename__ = 'people'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}

'''
User
Have title and release year
'''
class User(db.Model):  
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  e_mail = Column(String)
  address = Column(String)

  def __init__(self, e_mail, address=""):
    self.e_mail = e_mail
    self.address = address

  def format(self):
    return {
      'id': self.id,
      'e_mail': self.e_mail,
      'address': self.address}