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

# use world geodesic survey 1984 spatial coordinates
wgs84 <- "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0"
projection(rast) <- CRS(wgs84)

# load MSA shapefiles and data from US Census Bureau
shp = "cb_2014_us_cbsa_20m"
msa <- readOGR(dsn = path.expand(paste(imagery, shp, sep="/")), layer = shp)
projection(msa) <- CRS(wgs84)

# add population data for each MSA
msa_pop <- read.csv("http://www.census.gov/popest/data/metro/totals/2014/files/CBSA-EST2014-alldata.csv")
msa_pop <- msa_pop[msa_pop$LSAD=="Metropolitan Statistical Area",]
msa_pop <- msa_pop[order(msa_pop$POPESTIMATE2014),]
msa_pop$NAME <- as.character(msa_pop$NAME)

# create a list of 35 most populated cities
cities <- c("New York, NY", "Los Angeles, CA","Chicago, IL", "Houston, TX",
            "Philadelphia, PA", "Phoenix, AZ", "San Antonio, TX", "San Diego, CA",     
            "Dallas, TX", "San Jose, CA", "Austin, TX", "Jacksonville, FL",
            "San Francisco, CA", "Indianapolis, IN", "Columbus, OH", "Fort Worth, TX",
            "Charlotte, NC", "Detroit, MI", "El Paso, TX", "Seattle, WA",
            "Denver, CO","Washington, DC", "Memphis, TN", "Boston, MA",
            "Nashville, TN", "Baltimore, MD", "Oklahoma City, OK", "Portland, OR",
            "Las Vegas, NV", "Louisville, KY","Milwaukee, WI","Albuquerque, NM",
            "Tucson, AZ","Fresno, CA","Sacramento, CA")

# set up graph display (no margins, 7 rows by 5 columns)
par(mai=c(0,0,0,0),mfrow = c(7,5),bg='#001a4d', bty='n')

# use k-means clustering to bin light intensities
coords <- data.frame()

for(i in 1:length(cities)){
  
  # get bounds of city from google maps data
  temp_coord <- geocode(cities[i], source = "google")
  coords <- rbind(coords,temp_coord)
  
  e <- extent(temp_coord$lon - 1, temp_coord$lon + 1,
              temp_coord$lat - 0.25, temp_coord$lat + 0.25)
  rc <- crop(rast, e)    
  
  # calculate rescale brackets
  sampled <- as.vector(rc)
  clusters <- 15
  clust <- kmeans(sampled,clusters)$cluster
  combined <- as.data.frame(cbind(sampled,clust))
  brk <- sort(aggregate(combined[,1], list(combined[,2]), max)[,2])
  
  # plot data
  plot(rc, breaks=brk, col=colorRampPalette(c("#001a4d","#0066FF", "yellow"))(clusters), 
       legend=F,yaxt='n',xaxt='n',frame = F, asp=1.5)
  text(temp_coord$lon ,temp_coord$lat + 0.15,
       substr(cities[i],1,regexpr(",",cities[i])-1), 
       col="white", cex=1.25)
  
  rm(combined)
}


