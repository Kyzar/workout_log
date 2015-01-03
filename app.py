import os
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

#--------------- initialization ---------------#
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('development_config.py')


#--------------- controllers ---------------#
# show all entries
@app.route('/')
def index():
  cur = g.db.execute('select title, text from entries order by id desc')
  entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
  return render_template('index.html', entries=entries)

# # add new entry to database and redirect to all entries
# @app.route('/add', methods=['POST'])
# def add_entry():
#   if not session.get('logged_in'):
#     abort(401)
#   g.db.execute('insert into entries (title, text) values (?, ?)',
#               [request.form['title'], request.form['text']])
#   g.db.commit()
#   flash('New entry was successfully posted')
#   return redirect(url_for('index'))

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

#--------------- helper methods ---------------#
def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
      db.commit()

# returns list of results or first result if one=True
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
  db = getattr(g, 'db', None)
  if db is not None:
      db.close()


#--------------- launch ---------------#
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  init_db()
  app.run(host='0.0.0.0', port=port)