import flask
from flask import Flask, render_template
import json
import navigate

app = Flask(__name__)

DEBUG = True

@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/circles')
def circles():
    return render_template('circles.html')


@app.route('/data')
def data():
    return flask.jsonify(
        results = navigate.list_dir(navigate.get_home() + '/Projects/sos/apps')
        )


@app.route('/circles-data')
def circles_data():
    return flask.jsonify(
        results=navigate.path_to_tree(navigate.get_home() + '/Projects/sos/apps')
        )


if __name__ == '__main__':
    app.run(debug=True)
