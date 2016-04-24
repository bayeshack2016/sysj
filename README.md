# Night Lights

Explore: https://nightlights.terminal.com/

Example: Take a look at the growth in Loving, Texas from 2014 to 2016 (this is the leading county in population growth and net domestic migration rate in the US).

![VIIRS Suomi NPP satellite US 2012](data/nightlights.jpg)

Bayes Hack 2016

Team: 
- Yang Hong (yanghong.ee `@`gmail.com)
- Sasha Targ (sasha.targ `@` gmail.com)
- Steven Troxler (steven.troxler `@` gmail.com)
- Jeff Wu (wuthefwasthat `@` gmail.com)

## Data sources

http://ngdc.noaa.gov/eog/viirs/download_monthly.html

Also see `data/`.

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

- show NTL (night-time light) data and change over time (give us 1 more hour and we'll have these change in infrared light heatmaps done!)
- analyze whole world (using world bank PPP/CPI data), with focus on developing countries (NTL should be stronger signal there than in developed countries)
- show entire country view for state-to-state comparisons
- show entire state view for county-to-county comparisons
- automated pipeline that takes in raw VIIRS images, and generates both NTL statistics and powers the web app for data exploration
