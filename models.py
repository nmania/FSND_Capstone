from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
import babel

database_path = os.environ.get('DATABASE_URL')

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
    db.create_all()


'''
Movie
Has title and release date
'''
class Movie(db.Model):  
  __tablename__ = 'Movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  releaseDate = Column(db.DateTime)

  def __init__(self, title, releaseDate):
    self.title = title
    self.releaseDate = releaseDate

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'releaseDate': self.releaseDate
      }

'''
Actor
Has name, age, and gender
'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
      }