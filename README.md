Bayes Hack 2016 project

Team: Yang Hong, Sasha Targ, Steven Troxler, Jeff Wu

## Night Lights
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
