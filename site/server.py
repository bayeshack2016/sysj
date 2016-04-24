import random
import flask
from flask import Flask, render_template, request
import os
import usdatalib as usdata

mock = False

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

@app.route('/county_info')
def county_info():
    countystring = request.args.get('county')
    monthstring = request.args.get('month')

    county, state = map(lambda x: x.strip(), countystring.split(','))
    year, month = monthstring.split('/')

    info = {
        'pop': usdata.get_pop_from_county(county, state, year),
        'income': usdata.get_income_from_county(county, state, year),
        'gdp': usdata.get_gdp_from_state(state, year),
        'pce': usdata.get_pce_from_state(state, year),
    }
    return flask.jsonify(
        info=info
    )

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

    points = []
    bounds = None

    if mock:
        latmin = 37.782551
        lngmin = -121.445368
        bounds = {
            'lat': { 'min': latmin, 'max': latmin + 1 },
            'lng': { 'min': lngmin, 'max': lngmin + 1 },
        }
        points = [
            {'lat': latmin + random.random(), 'lng': lngmin + random.random(), 'intensity': random.random()}
            for _ in range(500)
        ]

    else:
        geoj, affine, bbox, _, mask = dao.get_county(county, month=month, which='raster')
        for i, j, val in data.get_2d_array_iter(bbox, mask):
            lat, lon = data.px_to_coords(i, j, affine)
            points.append({
                'lat': lat,
                'lng': lon,
                'intensity': float(val),
            })

    if bounds is None:
        bounds = {
            'lat': {
                'min': min([x['lat'] for x in points]),
                'max': max([x['lat'] for x in points])
            },
            'lng': {
                'min': min([x['lng'] for x in points]),
            'max': max([x['lng'] for x in points])
            },
        }

    return flask.jsonify(
        bounds = bounds,
        points = points,
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
