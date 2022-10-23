#!/usr/bin/python3
'''
This script records operations specific
to states route.
'''

from api.v1.views import app_views
from flask import json, abort, request, make_response
from models import storage
from models.state import State


# Bind function view to route /api/v1/states by using GET method
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def fetch_states():
    '''
    Fetch and return all state entries/resources

    Args:
        No required arguments
    Returns:
        Return list of all states obj in json for successfail.
    '''
    collection = storage.all(State)
    states = [state.to_dict() for state in collection.values()]
    response = json.dumps(states, indent=2)
    response = make_response(response)
    response.mimetype = 'application/json'
    return response


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def fetch_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    response = json.dumps(state.to_dict(), indent=2)
    response = make_response(response)
    response.mimetype = 'application/json'
    return response


# Bind function view to route /api/v1/<state_id> by using DELETE method
@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_state(state_id):
    '''
    Delete a state resource whose state_id is specified
    Args:
        state_id (str value key): Accept state's id
    Returns:
        return empty dictionary for success, error in json for fail
    '''
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()
    response = json.dumps({}, indent=2)
    response = make_response(response)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response


# Bind function view to route /api/v1/<state_id> by using POST method
@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    '''
    Add an entry to states table provided it's application/json
    formatted.
    Args:
        No required argument parameter
    Returns:
        Return 201 code for success, 400 for fail
    '''
    #: parsed post data
    data = request.get_json()

    # Check if the data format is acceptable and has
    # required attribute.
    response = ''
    if type(data).__name__ != 'dict':
        return make_response({'error': 'Not a JSON'}, 400)
    elif len(data) == 0 and type(data).__name__ == 'dict':
        return make_response({'error': 'Missing name'}, 400)
    elif type(data).__name__ == 'dict' and 'name' not in data:
        return make_response({'error': 'Missing name'}, 400)

    state = State(**data)
    state.save()
    response = json.dumps(state.to_dict(), indent=2)
    response = make_response(response)
    response.mimetype = 'application/json'
    response.status_code = 201
    return response


# Bind function view to route /api/v1/<state_id> by using PUT method
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''
    Update State modify/edit pre-existing State
    instance's attribute
    Args:
        state_id (str): Stores State instance id
    Returns:
        Return State obj with status code 200 on success
    '''
    #: State instance: Keeps reference to retrieved State instance
    state = storage.get(State, state_id)

    # Check the post data for application/json format
    # and if it has name attribute
    if not state:
        abort(404)
    data = request.get_json()

    if not data:
        abort(400, description='Not a JSON')
    elif 'name' not in data:
        abort(400, description='Missing name')

    skips = ['id', 'created_at', 'updated_at']
    for (key, value) in data.items():
        if key not in skips:
            setattr(state, key, value)

    state.save()
    response = json.dumps(state.to_dict(), indent=2)
    response = make_response(response)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response
