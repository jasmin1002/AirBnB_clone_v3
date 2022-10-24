#!/usr/bin/python3
'''
Base blueprint config file
'''

from flask import Blueprint

# application blueprint object
#: app_views: Stores reference to blueprint instance obj
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# import operations specific to each route
# or endpoint.
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
