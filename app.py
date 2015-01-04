import os
import time
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy


#--------------- initialization ---------------#
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('development_config.py')
db = SQLAlchemy(app)
from models import *

#--------------- controllers ---------------#
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

# if GET -> load login page
# if POST -> attempt to log user in
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

#--------------- launch ---------------#
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)