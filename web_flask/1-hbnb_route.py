#!/usr/bin/python3
'''A Flask application'''
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    return 'Hello HBNB!'


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    return 'HBNB'


if __name__ == '__main__':
    app.run()
