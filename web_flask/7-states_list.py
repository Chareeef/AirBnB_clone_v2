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


@app.route('/states_list', strict_slashes=False)
def states_list():
    '''Display all states in the database'''
    states = storage.all(State).values()
    states = sorted(states, key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
