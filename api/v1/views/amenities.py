#!/usr/bin/python3
'''
This script records operations specific
to amenities resources.
'''

from api.v1.views import app_views
from flask import abort, make_response, json, jsonify, request
from models import storage
from models.amenity import Amenity


# Bind view function to /api/v1/amenities/
@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False
)
@app_views.route(
    '/amenities',
    methods=['GET'],
    defaults={'amenity_id': None},
    strict_slashes=False
)
def get_amenities(**amenity_id):
    '''
    Retrieve all entries in amenities table
    Args:
        No required argument parameter
    Returns:
        Returns json list of amenities on success
    '''
    if amenity_id['amenity_id'] is None:
        amenities = storage.all(Amenity)
        data = [amenity.to_dict() for amenity in amenities]
        return jsonify(data)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    data = {}
    try:
        data = request.get_json()
    except Exception:
        pass
    if type(data).__name__ != 'dict':
        abort(400, 'Not a JSON')
        # return make_response({'error': 'Not a JSON'}, 400)
    elif type(data).__name__ == 'dict' and len(data) == 0:
        abort(400, 'Missing name')
        # return make_response({'error': 'Missing name'}, 400)
    elif type(data).__name__ == 'dict' and 'name' not in data:
        abort(400, 'Missing name')
        # return make_response({'error': 'Missing name'}, 400)
    elif type(data).__name__ == 'dict' and data['name'] == '':
        abort(400, 'Missing name')
        # return make_response({'error': 'Missing name'}, 400)
    amenity = Amenity(**data)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = {}
    try:
        data = request.get_json()
    except Exception:
        pass
    if type(data).__name__ != 'dict' or len(data) == 0:
        abort(400, description='Not a JSON')
        # return make_response({'error': 'Not a JSON'}, 400)
    skips = ['id', 'created_at', 'updated_at']
    for (key, value) in data.items():
        if key not in skips:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
