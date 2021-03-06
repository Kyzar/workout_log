import os
import time
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, \
     current_user, login_required


#--------------- initialization ---------------#
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('development_config.py')

# SQLAlchemy database
db = SQLAlchemy(app)
from models import * # import here to prevent circular ImportError

# Flask-Login initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


#--------------- routes ---------------#
'''
if GET -> load login page
if POST -> attempt to log user in
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
  # check user already logged in
  if not current_user.is_anonymous():
    flash('You are already logged in')
    return redirect(url_for('index'))

  if request.method == 'GET':
    return render_template('login.html')

  # POST request: log user in
  username = request.form['username']
  password = request.form['password']
  user = User.query.filter_by(username=username, password=password).first()

  if user is None:
    flash('Username or Password is invalid' , 'error')
    return redirect(url_for('login'))

  login_user(user, remember=True)
  flash("Logged in successfully.")
  return redirect(request.args.get('next') or url_for('index'))

'''
Log user out of account and redirect to index.
'''
@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You were logged out')
  return redirect(url_for('login'))

'''
Homepage.
TODO: Redirects to login/signup if not logged in.
'''
@app.route('/')
@login_required
def index():
  date = time.strftime('%a %b, %d')
  curr_time = time.strftime('%I:%M %p')
  return render_template('index.html', date=date, curr_time=curr_time)

'''
Add new entry to database and redirect to index.
'''
@app.route('/add', methods=['POST'])
@login_required
def add_entry():
  entry = Entry()
  entry.user = current_user
  # TODO :grab rows from request - start transaction, fail if any rows not added
  db.session.add(entry)
  db.commit()
  flash('Entry successfully saved');
  return redirect(url_for('index'))




#--------------- AJAX ---------------#
'''
Look up an exercise in entire db.
Requires: <string> name of exercise
Returns: JSON of exercise, or Error if not found
'''
@app.route('/lookup/exercise')
def lookup_exercise():
  query = request.args.get('exercise')
  if query == 'all':
    res = Exercise.query.order_by(Exercise.name).all()
  else:
    res = Exercise.query.filter_by(name=query).first()

  if res is None:
    # TODO: change to something... cleaner
    return 'Exercise not found', 404

  if query == 'all':
    return jsonify(results=[{
      'id': ex.id,
      'name': ex.name,
      'exerciseType': ex.exercise_type,
      'equipment': Equipment.query.get(ex.equipment_id).name
    } for ex in res])

  else:
    return jsonify(results={
      'id': res.id,
      'name': res.name,
      'exerciseType': res.exercise_type,
      'equipment': Equipment.query.get(res.equipment_id).name
    })

'''
Look up an equipment in entire db.
Requires: <string> name of equipment
Returns: JSON of equipment, or Error if not found
'''
@app.route('/lookup/equipment')
def lookup_equipment():
  query = request.args.get('equipment')
  if query == 'all':
    res = Equipment.query.order_by(Equipment.name).all()
  else:
    res = Equipment.query.filter_by(name=query).first()

  if res is None:
    return 'Exercise not found', 404

  if query == 'all':
    return jsonify(results=[{ 'id': eq.id, 'name': eq.name } for eq in res])
  else:
    return jsonify(results={ 'id': eq.id, 'name': res.name })

'''
Create an exercise in db.
Requires: <string> name of exercise,
          <bool> if exercise is strength or cardio,
          <int> id of equipment for this exercise
Returns: Success or error message.
'''
@app.route('/create', methods=['POST'])
def create():
  data = request.get_json(request.data)
  app.logger.debug(data)
  # TODO: validate all input present
  ex = Exercise(data['name'], data['exType'], data['equipmentId'])
  db.session.add(ex)
  db.session.commit()
  return '<p>Exercise successfully created</p>', 204


#--------------- launch ---------------#
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)

























