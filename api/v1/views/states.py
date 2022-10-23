#!/usr/bin/python3
'''
This script records operations specific
to states route.
'''

from api.v1.views import app_views
from flask import json, abort
from models import storage
from models.state import State


# Bind function view to route /api/v1/states
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def fetch_states():
    '''
    Fetch and return all state entry in states model
    Args:
        No argument is required
    Returns:
        Return list of all states obj in json
    '''
    collection = storage.all(State)
    states = [state.to_dict() for state in collection.values()]
    return json.dumps(states, indent=2)


# Bind function view to route /api/v1/states/<state_id>
@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def fetch_state_id(state_id):
    '''
    Fetch a state by identification key, state_id
    Args:
        state_id (str): A required state id key
    Return:
        return json state obj for success, 404 error (json) for fail
    '''
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    return json.dumps(state.to_dict(), indent=2)
