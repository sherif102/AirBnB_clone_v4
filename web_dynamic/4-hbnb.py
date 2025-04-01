#!/usr/bin/python3
"""flask app"""

from flask import Flask
from flask import render_template
import uuid
from models import storage, State, Amenity, Place, User


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception=None):
    storage.close()


@app.route("/4-hbnb", strict_slashes=False)
def hbnb():
    """return states list"""
    state_list = storage.all(State).values()
    amenity_list = storage.all(Amenity).values()
    place_list = storage.all(Place).values()
    user_list = storage.all(User).values()

    return render_template("4-hbnb.html", st_am={'states': state_list, 'amenities': amenity_list, 'places': place_list, 'users': user_list}, cache_id=uuid.uuid4())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
