Bayes Hack 2016

Team: Yang Hong, Sasha Targ, Steven Troxler, Jeff Wu

## Night Lights
https://nightlights.terminal.com/

![VIIRS Suomi NPP satellite US 2012](data/nightlights.jpg)

## Data sources

http://ngdc.noaa.gov/eog/viirs/download_monthly.html

## Setup

[Install libjpeg and zlib](http://stackoverflow.com/questions/34631806/fail-during-installation-of-pillow-python-module-in-linux)
```
brew install libjpeg zlib gdal
```

Install python libraries
```
pip install -r requirements.txt
```

## Run webserver

```
cd site
python server.py
```

## The future

- analyze whole world (using world bank PPP/CPI data), with focus on developing countries (NTL should be stronger signal there than in developed countries)
- show NTL (night-time light) data and change over time
- show entire country view for state-to-state comparisons
- show entire state view for county-to-county comparisons
- automated pipeline that takes in raw VIIRS images, and generates both NTL statistics and powers the web app for data exploration
