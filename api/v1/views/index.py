#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify

# Bind function view to route /status
@app_views.route('/status', strict_slashes=False)
def api_status():
    return jsonify({'status': 'OK'})
