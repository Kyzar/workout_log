import os
import time
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from flask.ext.sqlalchemy import SQLAlchemy


#--------------- initialization ---------------#
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('development_config.py')
db = SQLAlchemy(app)
# import here to prevent circular ImportError
from models import *


#--------------- routes ---------------#
@app.route('/')
def index():
  date = time.strftime('%a %b, %d')
  curr_time = time.strftime('%I:%M %p')
  # cur = g.db.execute('select title, text from entries order by id desc')
  # entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
  return render_template('index.html',
                          date=date,
                          curr_time=curr_time)

# add new entry to database and redirect to index
@app.route('/add', methods=['POST'])
def add_entry():
  if not session.get('logged_in'):
    abort(401)
  flash('Testing')
  return redirect(url_for('index'))

'''
if GET -> load login page
if POST -> attempt to log user in
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME']:
      error = 'Invalid username'
    elif request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid password'
    else:
      session['logged_in'] = True
      flash('You were logged in')
      return redirect(url_for('index'))

  # check user already logged in
  if 'logged_in' in session:
    flash('You are already logged in')
    return redirect(url_for('index'))

  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
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

@app.route('/create', methods=['POST'])
def create():
  data = request.get_json(request.data)
  app.logger.debug(data)
  # TODO: validate all input present
  ex = Exercise(data['exName'], data['exType'], data['equipmentId'])
  db.session.add(ex)
  db.session.commit()
  return '<p>Exercise successfully created</p>', 204


#--------------- launch ---------------#
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)

























