import os
from flask import Flask, render_template, request

# initialization
app = Flask(__name__)
app.debug = True

# controllers
@app.route("/")
@app.route("/<name>")
def index(name=None):
  return render_template('index.html', name=name)

# launch
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)