#!/usr/bin/python3
"""fetches all default RESTFul API actions"""
from api.v1.views import app_views
from api.v1.views import storage
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states', strict_slashes=False)
def get_states():
    """retrieve all states"""
    all_states = []
    states = storage.all(State)
    for state in states.values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_with_id(state_id):
    """retrieve a state"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a state"""
    states = storage.all(State)
    for state in states.values():
        if state.id == state_id:
            if state.cities:
                for city in state.cities:
                    storage.delete(city)
            try:
                storage.delete(state)
                storage.save()
                return jsonify({}), 200
            except Exception:
                return jsonify({"error": "Not found"}), 404
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """insert a state"""
    try:
        input_data = request.get_json()
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400

    if (check_input(input_data)) is not True:
        return (check_input(input_data))

    new_state = State(**input_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """update a state"""
    all_states = storage.all(State)
    for state in all_states.values():
        if state.id == state_id:
            try:
                data = request.get_json()

                for key, value in data.items():
                    if key in ['id', 'created_at', 'updated_at']:
                        continue
                    setattr(state, key, value)
                storage.save()
                return jsonify(state.to_dict()), 200
            except Exception:
                return jsonify({'error': 'Not a JSON'}), 400
    return jsonify({"error": "Not found"}), 404


def check_input(data_dict):
    """checks the input for correctness"""
    check_keys = ['name']
    for key in check_keys:
        if key not in list(data_dict.keys()):
            return jsonify({'error': 'Missing name'}), 400
    return True
