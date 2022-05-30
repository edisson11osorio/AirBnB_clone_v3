#!/usr/bin/python3
"""create a api"""


from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status_json():
    """status_json_response"""
    return jsonify({'status': 'OK'})
