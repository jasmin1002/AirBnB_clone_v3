#!/usr/bin/python3
'''
This script records operations specific
to cities route.
'''

from api.v1.views import app_views
from flask import abort, make_response, json, jsonify, request
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


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = ''
    try:
        data = request.get_json()
    except Exception:
        pass
    if type(data).__name__ != 'dict':
        return make_response({'error': 'Not a JSON'}, 400)
    elif type(data).__name__ == 'dict' and len(data) == 0:
        return make_response({'error': 'Missing name'}, 400)
    elif type(data).__name__ == 'dict' and 'name' not in data:
        return make_response({'error': 'Missing name'}, 400)
    elif type(data).__name__ == 'dict' and data['name'] == '':
        return make_response({'error': 'Missing name'}, 400)
    city = City(**data)
    city.state_id = state_id
    city.save()
    response = make_response(
        json.dumps(city.to_dict(), indent=2),
        201
    )
    response.mimetype = 'application/json'
    return response


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = {}
    try:
        data = request.get_json()
    except Exception:
        pass
    if type(data).__name__ != 'dict' or len(data) == 0:
        return make_response({'error': 'Not a JSON'}, 400)
    skips = ['id', 'state_id', 'created_at', 'updated_at']
    for (key, value) in data.items():
        if key not in skips:
            setattr(city, key, value)
    storage.save()
    response = make_response(
        json.dumps(city.to_dict(), indent=2),
        200
    )
    response.mimetype = 'application/json'
    return response
