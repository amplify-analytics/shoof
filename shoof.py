import flask
from flask import Flask, render_template
import json
import navigate

app = Flask(__name__)

DEBUG = True


@app.route('/')
def hello():
    path = flask.request.args.get('path', navigate.get_home())
    return render_template('index.html', path=path)


@app.route('/circles')
def circles():
    path = flask.request.args.get('path', None)
    if not path:
        path = navigate.get_home()
    return render_template('circles.html', path=path)


@app.route('/data')
def data():
    path = flask.request.args.get('path', None)
    if not path:
        path = navigate.get_home()
    return flask.jsonify(
        results = navigate.list_dir(path)
        )


@app.route('/circles-data')
def circles_data():
    path = flask.request.args.get('path', None)
    if not path:
        path = navigate.get_home()
    return flask.jsonify(
        results=navigate.path_to_tree(navigate.get_home() + '/Projects/sos/apps')
        )


if __name__ == '__main__':
    app.run(debug=True)
