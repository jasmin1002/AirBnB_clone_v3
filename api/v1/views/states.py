#!/usr/bin/python3
'''
This script records operations specific
to states route.
'''

from api.v1.views import app_views
from flask import json, abort, request
from models import storage
from models.state import State


# Bind function view to route /api/v1/states by using GET method
@app_views.route('/states', methods=['GET'], strict_slashes=False)
# @app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def fetch_states():
    '''
    Fetch and return all state entries/resources

    Args:
        No required arguments
    Returns:
        Return list of all states obj in json for successfail.
    '''
    '''if not state_id:'''
    collection = storage.all(State)
    states = [state.to_dict() for state in collection.values()]
    return json.dumps(states, indent=2)
    '''state = storage.get(State, state_id)
    if not state:
        abort(404)
    return json.dumps(state.to_dict(), indent=2)'''


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def fetch_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return json.dumps(state.to_dict(), indent=2)


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
    return json.dumps({}, indent=2), 200


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

    # Check if the data format is acceptable
    # and has required attribute(s)
    if not data:
        abort(400, description='Not a JSON')
    elif 'name' not in data:
        abort(400, description='Missing name')
    state = State(**data)
    state.save()
    return json.dumps(state.to_dict(), indent=2), 201


# Bind function view to route /api/v1/<state_id> by using PUT method
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()

    if not data:
        abort(400, description='Not a JSON')
    elif 'name' not in data:
        abort(400, description='Missing name')

    avoid = ['id', 'created_at', 'updated_at']
    for (key, value) in data.items():
        if key not in avoid:
            setattr(state, key, value)

    state.save()
    return json.dumps(state.to_dict(), indent=2), 200
