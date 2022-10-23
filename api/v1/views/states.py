#!/usr/bin/python3
'''
This script records operations specific
to states route.
'''

from api.v1.views import app_views
from flask import json
from models import storage
from models.state import State


# Bind function view to route /api/v1/states
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def fetch_states():
    '''
    Fetch and return all state entry in states model
    '''
    collection = storage.all(State)
    states = [state.to_dict() for state in collection.values()]
    return json.dumps(states, indent=2)
