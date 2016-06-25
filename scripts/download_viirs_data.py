"""
This script scrapes the NOAA website to download viirs data
"""

import requests
import os
import sh
from bs4 import BeautifulSoup

BASE_URL = 'http://mapserver.ngdc.noaa.gov/viirs_data/viirs_composite/v10'

# list a directory on the website
def list_path(path):
    r = requests.get(BASE_URL + path)
    parsed_html = BeautifulSoup(r.text, "lxml")
    rows = parsed_html.body.find('table').find_all('tr')

    # ignore first three rows, and last row
    rows = rows[3:-1]

    result = []
    for row in rows:
        href = row.find("a").attrs['href']
        if href is not None:
            result.append(href)
    return result

def get_time_periods():
    return [
        x[:-1] for x in
        list_path('/')
        if x.endswith('/')
    ]

def parse_time_period(time_period):
    year = int(time_period[:4])
    month = int(time_period[4:])
    return (year, month)

def parse_tile_filename(tile_file):
    parts = tile_file.split('_')
    tile = parts[3]
    return tile

def get_tile_files(time_period):
    # paths = list_path('/%s' % time_period)
    # assert paths == ['vcmcfg/', 'vcmslcfg/']
    paths = list_path('/%s/vcmcfg' % time_period)
    # ignores the png files
    return [path for path in paths if path.endswith('.tgz')]

# TILES:
# 00N060E - tile 6
# 00N060W - tile 5
# 00N180W - tile 4
# 75N060E - tile 3
# 75N060W - tile 2
# 75N180W - tile 1, north america

# download only data in february in north america
def download_data(output_folder, tiles=None, months=None, live=True):
    for time_period in get_time_periods():
        (year, month) = parse_time_period(time_period)
        if not (months is None or month in months):
            continue # not a month we care about
        for tile_file in get_tile_files(time_period):
            tile = parse_tile_filename(tile_file)
            if not (tiles is None or tile in tiles):
                continue # not a tile we care about
            url = '%s/%s/vcmcfg/%s' % (BASE_URL, time_period, tile_file)
            if live:
                # 'Warning: files to be downloaded are large'
                sh.tar(
                    sh.curl(url, _piped=True),
                    "xzv",
                    _cwd=output_folder
                )
            else:
                print 'Would download %s' % url

if __name__ == "__main__":
    output_folder = 'viirs_data'
    sh.mkdir('-p', output_folder)
    download_data(
        output_folder,
        tiles=['75N180W'],
        months=[2],
    )
