#!/usr/bin/python3
"""Create new view of Place objects that handles all RESTFul API actions"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.user import User
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_from_city(city_id):
    """Retrieves the list of all Places objects of a city"""
    city = storage.get('City', city_id)
    if city is not None:
        places_list = []
        for place in storage.all("Place").values():
            places_list.append(place.to_dict())
        return jsonify(places_list), 200
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def placeId_obj(place_id):
    """Retrieves a Place object."""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200

@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_placeId(place_id=None):
    """Deletes a Place object"""
    placeId_obj = storage.get("Place", place_id)
    if placeId_obj is None:
        abort(404)
    storage.delete(placeId_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object in a state"""
    city = storage.get('City', city_id)
    place_dict = request.get_json()
    if place_dict is None:
        abort(400, "Not a JSON")
    elif "user_id" not in place_dict():
        abort(400, "Missing user_id")
    elif "name" not in place_dict():
        abort(400, "Missing name")
    if city is not None:
        place_dict['city_id'] = city_id
        new_place = Place(**place_dict)
        new_place.save()
        storage.save()
        return jsonify(new_place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_placeId(place_id=None):
    """Updates a Place object"""
    placeId_to_update = storage.get('Place', place_id)
    if placeId_to_update is None:
        abort(404)
    placeId_dict = request.get_json()
    if placeId_dict is None:
        abort(400, "Not a JSON")
    for k, v in placeId_dict.items():
        if k in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            pass
        setattr(placeId_to_update, k, v)
    storage.save()
    return jsonify(placeId_to_update.to_dict()), 200
