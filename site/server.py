import random
import flask
from flask import Flask, render_template, request
import os

mock = True

if not mock:
    # relative imports
    import data
    dao = data.Data()

app = Flask(__name__, template_folder='views')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = True

# templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')

@app.route("/")
def index():
    return render_template('index.jade')

@app.route('/counties')
def counties():
    if mock:
        counties = ['Detroit, MI', 'Los Angeles, CA']
    else:
        counties = dao.counties
    return flask.jsonify(counties=counties)

@app.route('/months')
def months():
    if mock:
        months = ['2012/10', '2012/11']
    else:
        months = dao.months
    return flask.jsonify(months=months)

@app.route('/viirs_data')
def viirs_data():
    county = request.args.get('county')
    month = request.args.get('month')
    if mock:
        latmin = 37.782551
        lngmin = -121.445368
        return flask.jsonify(
            bounds = {
                'lat': { 'min': latmin, 'max': latmin + 1 },
                'lng': { 'min': lngmin, 'max': lngmin + 1 },
            },
            points = [
                {'lat': latmin + random.random(), 'lng': lngmin + random.random(), 'intensity': random.random()}
                for _ in range(500)
            ],
        )
    else:
        raise NotImplementedError("Oops")

if __name__ == "__main__":
    app.run()
