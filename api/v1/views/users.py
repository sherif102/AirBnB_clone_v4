#!/usr/bin/python3
"""fetches all default RESTFul API actions"""
from api.v1.views import app_views
from api.v1.views import storage
from models.city import City
from models.state import State
from models.user import User
from flask import jsonify, request


@app_views.route('/users', strict_slashes=False)
def get_users():
    """retrieve all users"""
    users = storage.all(User)
    all_user = []
    for user in list(users.values()):
        all_user.append(user.to_dict())
    return jsonify(all_user)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user_with_id(user_id):
    """retrieve a user"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete a user"""
    user = storage.get(User, user_id)
    if user:
        if user.places:
            for place in user.places:
                if place.reviews:
                    for review in place.reviews:
                        storage.delete(review)
                if place.amenities:
                    for amenity in place.amenities:
                        storage.delete(amenity)
                storage.delete(place)
        if user.reviews:
            for review in user.reviews:
                storage.delete(review)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """insert a user"""
    try:
        if not request.is_json:
            raise Exception
        input_data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'email' not in list(input_data.keys()):
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in list(input_data.keys()):
        return jsonify({'error': 'Missing password'}), 400

    new_user = User(**input_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """update a user"""
    user = storage.get(User, user_id)
    if not user:
        return jsonify({"error": "Not found"}), 404
    try:
        data = request.get_json()

        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400
    # return jsonify({"error": "Not found"}), 404


# def check_input(data_dict):
#     """checks the input for correctness"""
#     check_keys = ['email', 'password']
#     for key in check_keys:
#         if key not in list(data_dict.keys()):
#             text = f'{key}'
#             error = {"error": text}
#             return jsonify(error), 400
#     return True
