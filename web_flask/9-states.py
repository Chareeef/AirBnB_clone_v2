#!/usr/bin/python3
'''A flask app displaying states in a web page'''
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception=None):
    '''Remove the current SQLAlchemy Session after each request'''
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    '''Display all states in the database'''
    states = storage.all(State)

    if id:
        key = 'State.' + id
        if key in states.keys():
            state = states[key]
            state.cities = sorted(state.cities, key=lambda city: city.name)
            return render_template('9-states.html', with_id=True, state=state,
                                   found=True)
        else:
            return render_template('9-states.html', with_id=True, found=False)
    else:
        states = sorted(states.values(), key=lambda state: state.name)
        return render_template('9-states.html', with_id=False, states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
