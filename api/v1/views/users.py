#!/usr/bin/python3
"""Create a view User that handles RESTFul API actions"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import user, User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves all users"""
    all_users_list = []
    for user in storage.all("User").values():
        all_users_list.append(user.to_dict())
    return jsonify(all_users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_userId(user_id=None):
    """Retrieves a User object"""
    userId_obj = storage.get("User", user_id)
    if userId_obj is None:
        abort(404)
    return jsonify(userId_obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_userId(user_id=None):
    """Deletes a User object"""
    userId_obj = storage.get("User", user_id)
    if userId_obj is None:
        abort(404)
    storage.delete(userId_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    user_dict = request.get_json()
    if user_dict is None:
        abort(400, "Not a JSON")
    elif "email" not in user_dict.keys():
        abort(400, "Missing email")
    elif "password" not in user_dict.keys():
        abort(400, "Missing password")
    new_user = User(**user_dict)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_userId(user_id=None):
    """Updates a User object"""
    obj_userId = storage.get("User", user_id)
    if obj_userId is None:
        abort(404)
    userId_dict = request.get_json()
    if userId_dict is None:
        abort(400, "Not a JSON")
    for k, v in userId_dict.items():
        if k in ['id', 'email', 'created_at', 'updated_at']:
            pass
        setattr(obj_userId, k, v)
    storage.save()
    updated_userId = obj_userId.to_dict()
    return jsonify(updated_userId), 200
