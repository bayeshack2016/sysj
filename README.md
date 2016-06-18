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

For the lazy, there is a premade snapshot (including the data) [on Terminal.com](https://www.terminal.com/snapshot/1b57cc3d68112dcff922d1a1d98ae70de29161cb5080387e3d02377546e55ae0).

We assume you already have some basics, like `git`, `python2.7`, `pip`.

Otherwise:

1.  Git clone this repo
    ```git clone https://github.com/bayeshack2016/sysj```

1.  Download the python dependencies
    ```
    pip install -r requirements.txt
    ```

    NOTE: for the lxml module, you will need libxml
    e.g. on ubuntu:
    ```
    sudo apt-get update -y
    sudo apt-get install -y python-lxml
    ```

1. Download the data
   ``` python download_viirs_data.py ```

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
