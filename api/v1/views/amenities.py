#!/usr/bin/python3
"""handles all default RESTFul API actions"""


from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all amenities"""
    all_amenities_list = []
    for i in storage.all("Amenity").values():
        all_amenities_list.append(i.to_dict())
    return jsonify(all_amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenityId(amenity_id=None):
    """Retrieves a Amenity object"""
    amenityId_obj = storage.get("Amenity", amenity_id)
    if amenity_id is None:
        abort(404)
    return jsonify(amenityId_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenityId(amenity_id=None):
    """Deletes a Amenity object"""
    amenityId_obj = storage.get("Amenity", amenity_id)
    if amenityId_obj is None:
        abort(404)
    storage.delete(amenityId_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a Amenity object"""
    amenity_dict = request.get_json()
    if amenity_dict is None:
        abort(400, "Not a JSON")
    elif "name" not in amenity_dict.keys():
        abort(400, "Missing name")
    new_amenity = amenity.Amenity(**amenity_dict)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenityId(amenity_id=None):
    """Updates a Amenity object"""
    obj_amenityId = storage.get("Amenity", amenity_id)
    if obj_amenityId is None:
        abort(404)
    amenityId_dict = request.get_json()
    if amenityId_dict is None:
        abort(400, "Not a JSON")
    for k, v in amenityId_dict.items():
        if k in ['id', 'created_at', 'updated_at']:
            pass
        setattr(obj_amenityId, k, v)
    storage.save()
    updated_amenityId = obj_amenityId.to_dict()
    return jsonify(updated_amenityId), 200
