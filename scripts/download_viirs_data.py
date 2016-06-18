import requests
import os
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

# adapted from:
# https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def download_file(path, target_folder=None):
    if target_folder is None:
        target_folder = os.path.dirname(os.path.abspath(__file__))
    local_filename = path.split('/')[-1]
    local_file = '%s/%s' % (target_folder, local_filename)
    r = requests.get(BASE_URL + path, stream=True)
    with open(local_file, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

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
for time_period in get_time_periods():
    (year, month) = parse_time_period(time_period)
    if month == 2:
        print year, month
        for tile_file in get_tile_files(time_period):
            tile = parse_tile_filename(tile_file)
            if tile == '75N180W':
                download_file('/%s/vcmcfg/%s' % (time_period, tile_file))
