from app import db

'''
Entry model.
Requires:
Relationships: one-to-many with StrengthRow and CardioRow
'''
class Entry(db.Model):
  __tablename__ = 'entries'

  id = db.Column(db.Integer, primary_key=True)
  created_on = db.Column(db.DateTime, nullable=False, default=db.func.now())
  updated_on = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
  strength_rows = db.relationship('StrengthRow', backref='entry', lazy='dynamic')
  cardio_rows = db.relationship('CardioRow', backref='entry', lazy='dynamic')


'''
Strength row model. A row belongs to one entry.
Requires: id of entry,
          sets, reps, weight,
          id of exercise
Relationships: many-to-one with entry
'''
class StrengthRow(db.Model):
  __tablename__ = 'strengthrows'

  id = db.Column(db.Integer, primary_key=True)
  sets = db.Column(db.Integer)
  reps = db.Column(db.Integer)
  weight = db.Column(db.Integer)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
  entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'), nullable=False)

  def __init__(self, sets, reps, weight, exercise_id, entry_id):
    self.sets = sets
    self.reps = reps
    self.weight = weight
    self.exercise_id = exercise_id
    self.entry_id = entry_id

  def __repr__(self):
    exercise = Exercise.query.get(self.exercise_id).name
    return 'Sets: %s, Reps: %s, Weight: %s Exercise: %s' (self.sets, self.reps, self.weight, exercise)


'''
Cardio row model. A row belongs to one entry.
Requires: time - length of exercise,
          id of exercise,
          id of entry
Relationships: many-to-one with Entry
'''
class CardioRow(db.Model):
  __tablename__ = 'cardiorows'

  id = db.Column(db.Integer, primary_key=True)
  time = db.Column(db.DateTime, nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
  entry_id = db.Column(db.Integer, db.ForeignKey('entries.id'), nullable=False)

  def __init__(self, time, exercise_id, entry_id):
    self.time = time
    self.exercise_id = exercise_id
    self.entry_id = entry_id

  def __repr__(self):
    exercise = Exercise.query.get(self.exercise_id).name
    return 'Time: %s, Exercise: %s' (self.time, exercise)


'''
Exercise model.
Requires: name of exercise,
          type of exercise - True for strength, False for cardio,
          equipment_id - 1 by default (No equipment)
Relationships: many-to-one to Equipment
'''
class Exercise(db.Model):
  __tablename__ = 'exercises'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(40), unique=True, nullable=False)
  exercise_type = db.Column(db.String(10), default='strength', nullable=False)
  equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)

  def __init__(self, name, exercise_type, equipment_id=1):
    self.name = name
    self.exercise_type = exercise_type
    self.equipment_id = equipment_id

  def __repr__(self):
    return '%s, %s' %(self.name, exercise_type)

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