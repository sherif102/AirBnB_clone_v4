#!/usr/bin/python3
"""python flask app"""

from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views, jsonify
from os import getenv


app = Flask(__name__)
cores = CORS(app_views, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception=None):
    """cleanup connection after task done"""
    storage.close()


@app.errorhandler(404)
def error_404_not_found(error):
    """return customized 404 error message"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=getenv('HBNB_API_PORT', '5000'),
        threaded=True)
