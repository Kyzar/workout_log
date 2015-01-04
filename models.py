from app import db
from sqlalchemy.dialects.postgresql import JSON

class Exercise(db.Model):
  __tablename__ = 'exercises'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), unique=True)
  exercise_type = db.Column(db.Boolean()) # True for strength, False for cardio

  def __init__(self, name, exercise_type):
    self.name = name
    self.exercise_type = exercise_type

  def __repr__(self):
    string_of_type = 'Strength' if self.exercise_type else 'Cardio'
    return "%s, %s" %(self.name, string_of_type)

db.create_all()