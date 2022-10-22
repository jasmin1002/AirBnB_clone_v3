#!/usr/bin/python3
'''
This script records operation later perform by
blueprint when it extends flask application.
'''

from api.v1.views import app_views
from flask import jsonify


# Bind function view to route /status
@app_views.route('/status', strict_slashes=False)
def api_status():
    '''Bind function view to endpoint /status'''
    return jsonify({'status': 'OK'})
