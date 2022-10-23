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
    Fetch and return all state entries/resources

    Args:
        No required arguments
    Returns:
        Return list of all states obj in json for successfail.
    '''
    collection = storage.all(State)
    states = [state.to_dict() for state in collection.values()]
    return json.dumps(states, indent=2)


# Bind function view to route /api/v1/<state_id>
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def fetch_state(state_id):
    '''
    Fetch and return a state resource whose state_id is specified
    Args:
        state_id (str value key): Accept state's id
    Returns:
        return state obj for success, error in json for fail
    '''
    
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        return json.dumps(state.to_dict(), indent=2)
