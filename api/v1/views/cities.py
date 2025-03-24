#!/usr/bin/python3
"""fetches all default RESTFul API actions"""
from api.v1.views import app_views
from api.v1.views import storage
from models.city import City
from models.state import State
from flask import jsonify, request


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_of_a_state(state_id):
    """retrieve all cities in a state"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    if len(state.cities) > 0:
        all_cities = []
        for city in state.cities:
            all_cities.append(city.to_dict())
        return jsonify(all_cities)
    else:
        return jsonify([])


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city_with_id(city_id):
    """retrieve a city"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete a state"""
    city = storage.get(City, city_id)
    if city:
        if city.places:
            for place in city.places:
                if place.reviews:
                    for review in place.reviews:
                        storage.delete(review)
                if place.amenities:
                    for amenity in place.amenities:
                        storage.delete(amenity)
                storage.delete(place)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """insert a state"""
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "Not found"}), 404
    try:
        input_data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if (check_input(input_data)) is not True:
        return (check_input(input_data))

    new_city = City(state_id=state_id, **input_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """update a state"""
    city = storage.get(City, city_id)
    if not city:
        return jsonify({"error": "Not found"}), 404
    try:
        data = request.get_json()

        for key, value in data.items():
            if key in ['id', 'created_at', 'updated_at']:
                continue
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
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
