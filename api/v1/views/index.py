#!/usr/bin/python3
'''
This script records operation later perform by
blueprint when it extends flask application.
'''

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
from models.place import Place

#: Airbnb model tables
models = {
            'amenity': Amenity,
            'city': City,
            'review': Review,
            'state': State,
            'user': User,
            'place': Place
        }


# Bind function view to route /status
@app_views.route('/status', strict_slashes=False)
def api_status():
    '''Bind function view to endpoint /status'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False)
def resource_stats():
    '''
    Bind function view to endpoint /stats and
    give number of entry in each Airbnb's table
    '''
    stats = {}

    for (key, value) in models.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
