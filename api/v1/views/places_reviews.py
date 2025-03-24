#!/usr/bin/python3
"""fetches all default RESTFul API actions"""
from api.v1.views import app_views
from api.v1.views import storage
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
from models.review import Review
from flask import jsonify, request


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_all_reviews(place_id):
    """retrieve all reviews by place"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    if len(place.reviews) > 0:
        all_reviews = []
        for review in place.reviews:
            all_reviews.append(review.to_dict())
        return jsonify(all_reviews)
    else:
        return jsonify([])


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review_with_id(review_id):
    """retrieve a review"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a review"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """insert a place"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    try:
        if not request.is_json:
            raise Exception
        input_data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if "user_id" not in input_data:
        return jsonify({'error': 'Missing user_id'}), 400
    if "text" not in input_data:
        return jsonify({'error': 'Missing text'}), 400

    user = storage.get(User, input_data["user_id"])
    if not user:
        return jsonify({"error": "Not found"}), 404

    new_review = Review(place_id=place_id, **input_data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """update a place"""
    review = storage.get(Review, review_id)
    if not review:
        return jsonify({"error": "Not found"}), 404
    try:
        if not request.is_json:
            raise Exception
        data = request.get_json()

        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400
    # return jsonify({"error": "Not found"}), 404


# def check_input(data_dict):
#     """checks the input for correctness"""
#     check_keys = ['name']
#     for key in check_keys:
#         if key not in list(data_dict.keys()):
#             return jsonify({'error': 'Missing name'}), 400
#     return True
