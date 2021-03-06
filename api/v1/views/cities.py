#!/usr/bin/python3
"""Create new view of City objects that handles all RESTFul API actions"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_from_state(state_id):
    """Retrieves the list of all City objects of a state"""
    state = storage.get('State', state_id)
    if state is not None:
        cities_list = []
        for city in state.cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list), 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_obj(city_id):
    """Retrieves a City object."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_cityId(city_id=None):
    """Deletes a City object"""
    cityId_obj = storage.get("City", city_id)
    if cityId_obj is None:
        abort(404)
    storage.delete(cityId_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object in a state"""
    state = storage.get('State', state_id)
    city_dict = request.get_json()
    if city_dict is None:
        abort(400, 'Not a JSON')
    elif "name" not in city_dict():
        abort(400, 'Missing name')
    if state is not None:
        city_dict['state_id'] = state_id
        new_city = City(**city_dict)
        new_city.save()
        storage.save()
        return jsonify(new_city.to_dict()), 201
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_cityId(city_id=None):
    """Updates a City object"""
    cityId_to_update = storage.get('City', city_id)
    if cityId_to_update is None:
        abort(404)
    cityId_dict = request.get_json()
    if cityId_dict is None:
        abort(400, "Not a JSON")
    for k, v in cityId_dict.items():
        if k in ['id', 'state_id', 'created_at', 'updated_at']:
            pass
        setattr(cityId_to_update, k, v)
    storage.save()
    return jsonify(cityId_to_update.to_dict()), 200
