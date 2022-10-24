#!/usr/bin/python3
'''
This script records operations specific
to cities route.
'''

from api.v1.views import app_views
from flask import abort, make_response, json
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
    if state is None:
        abort(404)
    #: cities (list of dictionary): Stores all cities of a state
    cities = [city.to_dict() for city in state.cities]
    # Convert list to string
    response = json.dumps(cities, indent=2)
    # Convert string to Response type
    response = make_response(response)
    # Set mime type to application/json
    response.mimetype = 'application/json'
    return response


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def fetch_city(city_id):
    '''
    Retrieve a city from city resources by city ID
    Args:
        city_id (str): argument parameter to city ID
    Return:
        Returns json city with 200 ok for success, otherwise error 404
    '''
    #: city (City instance): Keeps reference to City instance obj
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    # Convert dict_city to string
    response = json.dumps(city.to_dict(), indent=2)
    # convert string to Response type
    response = make_response(response)
    response.mimetype = 'application/json'
    return response
