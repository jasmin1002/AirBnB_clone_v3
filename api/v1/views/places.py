#!/usr/bin/python3
'''
This records operations specific to places
resources/table
'''

from api.v1.views import app_views
from flask import Flask, jsonify, request
from models import storage
from models.city import City
from models.place import Place


# Bind view function to /api/v1/cities/<city_id>/places
@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET'],
    strict_slashes=False
)
def fetch_places(city_id):
    city = storage.get(City, city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    else:
        abort(404)


# Bind view function to /api/v1/places/<place_id>
@app_views.route(
    '/places/<place_id>',
    methods=['GET'],
    strict_slashes=False
)
def fetch_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


# Bind view function to /api/v1/places/<place_id>
# on DELETE
@app_views.route(
    '/places/<place_id>',
    method=['DELETE'],
    strict_slashes=False
)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


# Bind view function to /api/v1/cities/<city_id>/places
# on POST request
@app_views.route(
    '/cities/<city_id>/places',
    method=['POST'],
    strict_slashes=False
)
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = {}
    try:
        data = request.get_json()
    except Exception:
        pass

    if type(data).__name__ != 'dict':
        abort(400, description='Not a JSON')
    elif 'user_id' not in data:
        abort(400, description='Missing user_id')
    elif len(data) == 0 or 'name' not in data:
        abort(400, description='Missing name')
    elif data['name'] == '':
        abort(400, description='Missing name')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


# Bind view function to /api/v1/places/<place_id>
# on PUT request
@app_views.route(
    '/places/<place_id>',
    method=['PUT'],
    strict_slashes=False
)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = {}
    try:
        data = request.get_json()
    except Exception:
        pass
    if type(data).__name__ != 'dict' or len(data) == 0:
        abort(400, description='Not a JSON')
    skips = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for (key, value) in data.items():
        if key not in skips:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())
