import random
import flask
from flask import Flask, render_template, request
import os

# relative imports
import data

app = Flask(__name__, template_folder='views')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = True

dao = data.Data()

# templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')

@app.route("/")
def index():
    return render_template('index.jade')

@app.route('/counties')
def counties():
    counties = dao.counties
    return flask.jsonify(counties=counties)

@app.route('/months')
def months():
    months = dao.months
    return flask.jsonify(months=months)

@app.route('/viirs_data')
def viirs_data():
    county = request.args.get('county')
    month = request.args.get('month')
    print "COUNTY", county
    print "MONTH", month
    return flask.jsonify(
        points = [
            {'lat': 37.782551 + random.random(), 'lng': -122.445368 + random.random(), 'intensity': random.random()}
            for _ in range(500)
        ]
    )

if __name__ == "__main__":
    app.run()
