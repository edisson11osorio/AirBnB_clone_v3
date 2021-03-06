#!/usr/bin/python3
"""
start API
"""

from flask import Flask
from models import storage

from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(self):
    """closes storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """returns a JSON-formatted 404"""
    return {"error": "Not found"}, 404


if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=api_host, port=int(api_port), debug=True, threaded=True)
