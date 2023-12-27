#!/usr/bin/python3
'''A flask app displaying states in a web page'''
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity


app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception=None):
    '''Remove the current SQLAlchemy Session after each request'''
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    '''Display an AirBnB clone pages with filters feeded by our database'''
    states = storage.all(State).values()
    states = list(sorted(states, key=lambda state: state.name))

    for s in states:
        s.cities = list(sorted(s.cities, key=lambda city: city.name))

    amenities = storage.all(Amenity).values()
    amenities = list(sorted(amenities, key=lambda amenity: amenity.name))

    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
