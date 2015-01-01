import os
from Flask import Flask, send_from_directory

# initialization
app = Flask(__name__)
app.config.update(
  DEBUG = True
)

# controllers
@app.route("/")
def index():
  return "Hello test"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')

# launch
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)