#!/usr/bin/python3
"""Create new view of State objects that handles all RESTFul API actions"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    all_states_list = []
    for i in storage.all("State").values():
        all_states_list.append(i.to_dict())
    return jsonify(all_states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def stateId(state_id=None):
    """Retrieves a State object"""
    stateId_obj = storage.get("State", state_id)
    if state_id is None:
        abort(404)
    return jsonify(stateId_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_stateId(state_id=None):
    """Deletes a State object"""
    stateId_obj = storage.get("State", state_id)
    if stateId_obj is None:
        abort(404)
    storage.delete(stateId_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    state_dict = request.get_json()
    if state_dict is None:
        abort(400, "Not a JSON")
    elif "name" not in state_dict.keys():
        abort(400, "Missing name")
    new_state = state.State(**state_dict)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_stateId(state_id=None):
    """Updates a State object"""
    obj_stateId = storage.get("State", state_id)
    if obj_stateId is None:
        abort(404)
    stateId_dict = request.get_json()
    if stateId_dict is None:
        abort(400, "Not a JSON")
    for k, v in stateId_dict.items():
        if k in ['id', 'created_at', 'updated_at']:
            pass
        setattr(obj_stateId, k, v)
    storage.save()
    updated_stateId = obj_stateId.to_dict()
    return jsonify(updated_stateId), 200
