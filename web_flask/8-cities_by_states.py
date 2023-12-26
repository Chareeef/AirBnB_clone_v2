#!/usr/bin/python3
'''A flask app displaying cities by states in a web page'''
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception=None):
    '''Remove the current SQLAlchemy Session after each request'''
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    '''Display all states and their cities in the database'''
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)

    for s in states:
        s.cities = sorted(s.cities, key=lambda city: city.name)

    return render_template('8-cities_by_states.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
