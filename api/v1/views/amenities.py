#!/usr/bin/python3
"""fetches all default RESTFul API actions"""
from api.v1.views import app_views
from api.v1.views import storage
from models.city import City
from models.state import State
from models.amenity import Amenity
from flask import jsonify, request


@app_views.route('/amenities', strict_slashes=False)
def get_all_amenity():
    """retrieve all amenities"""
    amenities = storage.all(Amenity)
    all_amenity = []
    for amenity in list(amenities.values()):
        all_amenity.append(amenity.to_dict())
    return jsonify(all_amenity)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """retrieve an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """insert an amenity"""
    try:
        input_data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if (check_input(input_data)) is not True:
        return (check_input(input_data))

    new_amenity = Amenity(**input_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update a state"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    try:
        data = request.get_json()

        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400
    # return jsonify({"error": "Not found"}), 404


def check_input(data_dict):
    """checks the input for correctness"""
    check_keys = ['name']
    for key in check_keys:
        if key not in list(data_dict.keys()):
            return jsonify({'error': 'Missing name'}), 400
    return True
