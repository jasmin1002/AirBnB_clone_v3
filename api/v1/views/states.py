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
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def fetch_states(state_id=None):
    '''
    Fetch and return either all state entries/resources
    or a state with specified state's id
    Args:
        state_id (optional str value): Accept state's id or None default
    Returns:
        Return either list of all states obj or an entry in json for
        success, 404 error response for fail.
    '''
    if not state_id:
        collection = storage.all(State)
        states = [state.to_dict() for state in collection.values()]
        return json.dumps(states, indent=2)
    else:
        state = storage.get(State, state_id)
        if not state:
            return abort(404)
        return json.dumps(state.to_dict(), indent=2)
