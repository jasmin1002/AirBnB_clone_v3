#!/usr/bin/python3
'''
This script records operations specific
to cities route.
'''

from api.v1.views import app_views
from flask import json, make_response
from models import storage
from models.city import City
from models.state import State


# Bind view function to /api/v1/states/<state_id>/cities
@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False
)
def fetch_cities(state_id):
    '''
    Fetch cities belong to specified state by state ID
    Args:
        state_id (str): Stores state ID
    Returns:
        Returns json list of cities on success
    '''
    #: state (State instance): Keeps reference to State instance obj
    state = storage.get(State, state_id)
    #: cities (list of dictionary): Stores all cities of a state
    cities = [city.to_dict() for city in state.cities]
    # Convert list to string
    response = json.dumps(cities, indent=2)
    # Convert string to Response type
    response = make_response(response)
    # Set mime type to application/json
    response.mimetype = 'application/json'
    return response
