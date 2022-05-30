#!/usr/bin/python3
"""Create new view of State objects that handles all RESTFul API actions"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_all_states():
    """Retrieves the list of all State objects"""
    all_states_list = []
    for i in storage.all("State").values():
        all_states_list.append(i.to_dict())
    return jsonify(all_states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id=None):
    """Retrieves a State object"""
    stateId_obj = storage.get("State", state_id)
    if state_id is None:
        abort(404)
    return jsonify(stateId_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_id(state_id=None):
    """Deletes a State object"""
    stateId_obj = storage.get("State", state_id)
    if state_id is None:
        abort(404)
    storage.delete(stateId_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    state_obj = request.get_json()
    if state_obj is None:
        abort(400, "Not a JSON")
    elif "name" not in state_obj.keys():
        abort(400, "Missing name")
    new_state = state.State(**state_obj)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_id(state_id=None):
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
