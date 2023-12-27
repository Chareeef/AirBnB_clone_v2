#!/usr/bin/python3
'''A flask app displaying AirBnB clone page'''
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User


app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception=None):
    '''Remove the current SQLAlchemy Session after each request'''
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    '''Display the entire AirBnB clone page feeded by our database'''
    states = storage.all(State).values()
    states = list(sorted(states, key=lambda state: state.name))

    for s in states:
        s.cities = list(sorted(s.cities, key=lambda city: city.name))

    amenities = storage.all(Amenity).values()
    amenities = list(sorted(amenities, key=lambda amenity: amenity.name))

    places = storage.all(Place).values()
    places = list(sorted(places, key=lambda place: place.name))

    users = storage.all(User)

    for p in places:
        owner_key = 'User.' + p.user_id
        owner = users.get(owner_key)
        p.owner_name = owner.first_name + ' ' + owner.last_name

    return render_template('100-hbnb.html', states=states,
                           amenities=amenities, places=places)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
