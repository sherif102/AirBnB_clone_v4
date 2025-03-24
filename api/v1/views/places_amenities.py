#!/usr/bin/python3
"""fetches all default RESTFul API actions"""
from api.v1.views import app_views
from api.v1.views import storage
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, request


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def get_amenity_by_place(place_id):
    """retrieve all amenities in a place"""
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({"error": "Not found"}), 404
    if len(place.amenities) > 0:
        all_amenities = []
        for amenity in place.amenities:
            all_amenities.append(amenity.to_dict())
        return jsonify(all_amenities)
    else:
        return jsonify([])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """delete a amenity"""
    try:
        place = storage.get(Place, place_id)
        amenity = storage.get(Amenity, amenity_id)
        amenity_present = amenity in place.amenities
    except Exception:
        return jsonify({"error": "Not found"}), 404
    if place and amenity and amenity_present:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """insert a amenity into place"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place and amenity:
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    return jsonify({"error": "Not found"}), 404
