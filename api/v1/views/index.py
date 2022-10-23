#!/usr/bin/python3
'''
This script records operation later perform by blueprint
through entry route when it extends flask application.
'''

from api.v1.views import app_views
from flask import json, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.state import State
from models.user import User
from models.place import Place

#: Airbnb model tables
tables = {
            'amenities': Amenity,
            'cities': City,
            'reviews': Review,
            'states': State,
            'users': User,
            'places': Place
        }


# Bind function view to route /status
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    '''Bind function view to endpoint /status'''
    response = json.dumps({'status': 'OK'}, indent=2)
    response = make_response(response)
    response.mimetype = 'application/json'
    return response


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def resource_stats():
    '''
    Bind function view to endpoint /stats and
    give number of entry in each Airbnb's table
    '''
    stats = {}

    for (key, value) in tables.items():
        stats[key] = storage.count(value)
    return json.dumps(stats, indent=2)
