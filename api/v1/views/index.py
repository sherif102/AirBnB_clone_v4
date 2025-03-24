#!/usr/bin/python3
"""index app"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify


@app_views.route('/status')
def status():
    """fetch the response header for OK"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """fetches the stats of the data"""
    classes = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, value in classes.items():
        classes[key] = storage.count(value)
    return jsonify(classes)
