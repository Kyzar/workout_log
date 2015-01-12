from app import db

'''
Equipment model.
Requires: name of equipment
Relationships: one-to-many to Exercise
'''
class Equipment(db.Model):
  __tablename__ = 'equipment'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), unique=True, nullable=False)

  exercises = db.relationship('Exercise', backref='equipment', lazy='dynamic')

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.name

'''
Exercise model.
Requires: name of exercise
          type of exercise - True for strength, False for cardio
          equipment_id - 1 by default (No equipment)
Relationships: many-to-one to Equipment
'''
class Exercise(db.Model):
  __tablename__ = 'exercises'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), unique=True, nullable=False)
  exercise_type = db.Column(db.Boolean(), nullable=False)
  equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)

  def __init__(self, name, exercise_type, equipment='none'):
    self.name = name
    self.exercise_type = exercise_type

    # set equipment to none if not found, else set it to first result
    eq = Equipment.query.filter_by(name=equipment).first()
    if eq:
      self.equipment_id = eq.id
    else:
      self.equipment_id = Equipment.query.filter_by(name='none').first().id

  def __repr__(self):
    string_of_type = 'Strength' if self.exercise_type else 'Cardio'
    return "%s, %s" %(self.name, string_of_type)