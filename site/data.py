import json
import re
import os

import sh
import pandas as pd
import numpy as np
import rasterio
import rasterio.features
from affine import Affine
from shapely.geometry import shape

HOME = os.path.expanduser('~')
THIS_FILE_DIR = os.path.dirname(__file__)
OUR_REPO = sh.git('rev-parse', '--show-toplevel',
                  _cwd=THIS_FILE_DIR).stdout.strip()

INT_DATA_DIR = os.path.join(OUR_REPO, 'data')
EXT_DATA_DIR = os.path.join(HOME, 'bh', 'data')
SAT_DIR = os.path.join(EXT_DATA_DIR, 'satellite')
GEO_DIR = os.path.join(INT_DATA_DIR, 'geo')

# this is commented because we are currently only using counties, not metro
# areas
'''
# metropolitan shapefile
METRO_SHP = os.path.join(EXT_DATA_DIR, 'cb_2014_us_cbsa_20m.shp')
# metropolitan populations
METRO_POP = os.path.join(EXT_DATA_DIR,
                         'us_metropolitan_area_census_data_2014.csv')
'''

# county geo-json files
COUNTY_GJS = os.path.join(INT_DATA_DIR, 'us_counties_5m.json')

# State metadata, which is a | - separated file
STATE_META = os.path.join(INT_DATA_DIR, 'state.txt')


def coords_to_px(lat, lon, affine):
    """
    Given the affine mapping for a raster block, find the nearest
    """
    lat_px = int(np.round((lat - affine.f) / affine.e))
    lon_px = int(np.round((lon - affine.c) / affine.a))
    return lat_px, lon_px

def px_to_coords(lat_px, lon_px, affine):
    """
    Given the affine mapping for a raster block, find the nearest
    """
    lat = float(lat_px * affine.e + affine.f)
    lon = float(lon_px * affine.a + affine.c)
    return lat, lon

class Data(object):

    def __init__(self):
        self._image_paths = get_image_paths()
        self.months = sorted(self._image_paths.keys())
        self._state_meta = pd.read_csv(STATE_META, sep='|').set_index('STATE')
        self._counties = self._load_counties()
        self.counties = sorted(self._counties.keys())

    def get_county(self, county_name, month=None, which='geojson'):
        """
        For a county:
          - if `which` is "geojson", return a python dict of geojson data
          - if `which` is "raster", return a tuple of
            (geojson, affine_trans, bounding_box, masked_bounding_box)
            where
             - geojson is a dict of geojson for that county,
             - affine_trans is an Affine instance indicating how to map
               (lat, lng) pairs to pixel indices in `bounding_box`
             - bounding_box is a numpy array of pixels from satellite data
               covering a bounding box for that county
             - masked_bounding_box is the same as bounding_box, except that
               it is a numpy bitmasked array with the mask set only for those
               pixels which lie (at least partially) inside the actual
               county borders.
        """
        if which == 'geojson':
            return self._get_county_geojson(county_name)
        elif which == 'raster':
            try:
                raster_file = rasterio.open(self._image_paths[month], 'r')
                geoj = self._get_county_geojson(county_name)
                affine, bbox, mbbox, mask = get_sub_image(raster_file, geoj)
            except KeyError:
                raise ValueError("Unknown month %r" % month)
            return geoj, affine, bbox, mbbox, mask

    def state_meta(self, state_id):
        "Get a dict of metadata about a state"
        return dict(self._state_meta.loc[int(state_id)])

    # helper methods ----

    def _get_county_geojson(self, county_name):
        "Get the (python dict of) geojson for a county"
        return self._counties[county_name]

    # init helpers ----

    def _load_counties(self):
        """
        Return a dict that maps keys of the format
          'county_name, state_name'
        to geojson feature dicts.

        NOTE: we lose 7 counties in this mapping, presumably due to non-unique
        keys. We're going to ignore this issue for now.

        """
        raw_counties = load_county_geojson()['features']  # list of geo json
        county_name = lambda x: x['properties']['NAME']
        state_name = lambda x: self.state_meta(
            x['properties']['STATE']
        )['STATE_NAME']

        def get_name(county):
            return u'{}, {}'.format(county_name(county), state_name(county))

        return {get_name(cnty): cnty for cnty in raw_counties}


# raster processing tools -------------------------

def get_sub_image(raster_file, geo_feature):
    """
    Given
      - a rasterio file object, and
      - a (dict representing) a geo json feature
    we
      - use shapely to determine the boundaries of the feature
      - determine the upper left and lower right boundaries in the raster
        index (that is, the raw indices for the bounding box)
      - extract the raster data for just that bounding box
      - compute a new affine transformation (which is what gives us the mapping
        between lat/long coordinates and pixels) for the bounding box, from
        the transformation of the entire raster file
      - compute a numpy masked array indicating just the data within the
        borders of the feature
    We return
      - the raw pixel data for the bounding box, as a numpy array
      - the masked version of that data
      - the affine transformation

    Thanks to @star_is_here for the starting point of the code
    """
    # get a shapely geometry object from the feature
    geometry = shape(geo_feature['geometry'])
    # get pixel coordinates of the geometry's bounding box
    tl = raster_file.index(*geometry.bounds[0:2])
    br = raster_file.index(*geometry.bounds[2:4])
    # get the affine transformation appropriate for data from that bounding box
    t = raster_file.affine
    bb_affine = Affine(t.a, t.b, t.c+tl[1]*t.a, t.d, t.e, t.f+br[0]*t.e)
    # read the subset of the data into a numpy array
    raster_window = ((br[0], tl[0]+1), (tl[1], br[1]+1))
    bb_data = raster_file.read(1, window=raster_window)
    # compute the bitmask for inclusion, and make a masked version of bb_data
    containment_mask = rasterio.features.rasterize(
        [(geometry, 0)],
        out_shape=bb_data.shape,
        transform=bb_affine,
        fill=1,
        all_touched=True,
        dtype=np.uint8
    )
    mask = containment_mask.astype(bool)
    bb_masked = np.ma.array(data=bb_data, mask=mask)
    return bb_affine, bb_data, bb_masked, mask

def get_2d_array_iter(np_array, mask=None):
    for i in range(np_array.shape[0]):
        for j in range(np_array.shape[1]):
            if mask is None or not mask[i][j]:
                  yield i, j, np_array[i][j]

# utilities ----------------------------------------

def load_county_geojson():
    with open(COUNTY_GJS, 'r') as f:
        return json.load(f, encoding='latin-1')


def get_image_paths(sat_dir=SAT_DIR):
    """
    By listing contents of the satellite data dir, get a dict
    of 'yyyy/mm': file_path pairs indicating where to find each year and
    month of data
    """

    names = sh.ls(sat_dir).stdout.strip().split()
    names = filter(lambda x: x.endswith('.tif'), names)
    yms = [get_ym_from_fname(n) for n in names]
    keys = ['%04d/%02d' % (y, m) for y, m in yms]
    return {k: os.path.join(sat_dir, n) for k, n in zip(keys, names)}


def get_ym_from_fname(fname):
    "Get the year and month from a satellite image file's name"
    # the match is stard date in 'yyyymmdd' format
    start_date_str = re.findall('\\d+', fname)[0]
    year = int(start_date_str[:4])
    month = int(start_date_str[4:6])
    return year, month



############ script


