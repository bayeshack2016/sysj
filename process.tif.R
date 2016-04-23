# modified from https://commercedataservice.github.io/tutorial_viirs_part1/

library(doParallel)
library(foreach)
library(raster)
library(sp)
library(rgdal)
library(ggmap)
library(plotly)

# specify directory
imagery = '~/Desktop/VIIRS'

# load raster of first image
tifs = list.files(imagery, pattern = "\\.tif")
rast <- raster(paste(imagery, "/", tifs[1], sep=""))

# use world geodetic survey 1984 spatial coordinates
wgs84 <- "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0"
projection(rast) <- CRS(wgs84)

# load MSA shapefiles and data from US Census Bureau
shp = "cb_2014_us_cbsa_20m"
msa <- readOGR(dsn = path.expand(paste(imagery, shp, sep="/")), layer = shp)
projection(msa) <- CRS(wgs84)