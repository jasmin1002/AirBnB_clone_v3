#!/usr/bin/python3
'''
This script records operations specific
to users resources.
'''

from api.v1.views import app_views
from flask import abort, make_response, json, jsonify, request
from models import storage
from models.user import User


# Bind view function to /api/v1/amenities/
@app_views.route(
    '/users/<user_id>',
    methods=['GET'],
    strict_slashes=False
)
@app_views.route(
    '/users',
    methods=['GET'],
    defaults={'user_id': None},
    strict_slashes=False
)
def get_users(**user_id):
    '''
    Retrieve either an entry or all entries in users table
    Args:
        user_id (optional str): Stores None or user ID
    Returns:
        Returns json list of users or user obj on success
    '''
    if user_id['user_id'] is None:
        users = storage.all(User)
        data = [user.to_dict() for user in users]
        return jsonify(data)
    else:
        user = storage.get(User, user_id['user_id'])
        if user is None:
            abort(404)
        return jsonify(user.to_dict())


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_user(user_id):
    '''
    Delete a user specified by its user ID from
    users entries/table
    Args:
        user_id (str): Stores user ID
    Returns:
        Return empty dictionary with 200 code on success
        and error status code 404 on failure
    '''
    #: user (user obj): Keeps reference to retrieved User obj
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    Create and add user entry to users resource/table
    Args:
        No required argument parameter
    Returns:
        Returns newly created user with status code 201
        on success and 400 error code on failure.
    '''
    #: data (dict): Stores parsed json argument
    data = {}
    try:
        data = request.get_json()
    except Exception:
        pass
    # Check for structure and attribute of input json data
    if not data:
        return make_response('Not a JSON', 400)
    if 'email' not in data:
        return make_response('Missing email', 400)
    if 'password' not in data:
        return make_response('Missing password', 400)
    #: user (User obj): Stores reference to newly created
    # User obj
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_user(user_id):
    '''
    Modify the existing user entry in the user table
    Args:
        user_id (str): Stores user ID
    Returns:
        Return user obj with status code 200 on success
        and 404 error code on failure.
    '''
    #: user(User instance): Stores reference to select user
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    #: data(dict): Store reference of parsed json data
    data = {}
    try:
        data = request.get_json()
    except Exception:
        pass
    if not data:
        abort(400, description='Not a JSON')
    #: skips (list of str): Keeps list of ignored keys
    skips = ['id', 'email', 'created_at', 'updated_at']
    for (key, value) in data.items():
        if key not in skips:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
