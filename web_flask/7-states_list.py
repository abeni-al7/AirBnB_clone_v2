#!/usr/bin/python3
"""This module starts a flask web app"""
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Returns a list of all states"""
    states = storage.all('State')
    return render_template('7-states_list')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
