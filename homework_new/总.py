from flask import Flask
from flask_cors import CORS
from gevent import pywsgi
from history import history
from search import new_search
from user import user

app = Flask(__name__)
CORS(app)
app.register_blueprint(user)
app.register_blueprint(new_search)
app.register_blueprint(history)

s = pywsgi.WSGIServer(('0.0.0.0',8000), app)
s.serve_forever()