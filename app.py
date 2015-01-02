import os
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# initialization
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('development_config.py')

# controllers
@app.route("/")
@app.route("/<name>")
def index(name=None):
  return render_template('index.html', name=name)

# helper methods
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# launch
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  init_db()
  app.run(host='0.0.0.0', port=port)