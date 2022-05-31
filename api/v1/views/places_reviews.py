#!/usr/bin/python3
"""Create new view of Review objects that handles all RESTFul API actions"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Reviews objects of a place"""
    place = storage.get('Place', place_id)
    if place is not None:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list), 200
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_obj(review_id):
    """Retrieves a Review object."""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200

@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviewId(review_id=None):
    """Deletes a Review object"""
    reviewId_obj = storage.get("Review", review_id)
    if reviewId_obj is None:
        abort(404)
    storage.delete(reviewId_obj)
    storage.save()
    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object in a place"""
    review_dict = request.get_json()
    if review_dict is None:
        abort(400, 'Not a JSON')
    elif "text" not in review_dict():
        abort(400, 'Missing text')
    elif "user_id" not in review_dict():
        abort(400, 'Missing user_id')
    place = storage.get('Place', place_id)
    user = storage.get(request.get_json()['user_id'])
    if user is None:
        abort(404)
    if place is None:
        abort(404)
    review_dict['place_id'] = place_id
    new_review = Review(**review_dict)
    new_review.save()
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_reviewId(review_id=None):
    """Updates a Review object"""
    reviewId_to_update = storage.get('Review', review_id)
    if reviewId_to_update is None:
        abort(404)
    reviewId_dict = request.get_json()
    if reviewId_dict is None:
        abort(400, "Not a JSON")
    for k, v in reviewId_dict.items():
        if k in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            pass
        setattr(reviewId_to_update, k, v)
    storage.save()
    return jsonify(reviewId_to_update.to_dict()), 200
