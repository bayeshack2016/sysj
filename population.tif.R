# visualize US counties with the most change in population from July 2014 to July 2015
library(doParallel)
library(foreach)
library(raster)
library(sp)
library(rgdal)
library(ggmap)
library(plotly)

# specify directory
imagery = '~/Desktop/VIIRS'

# load rasters of images
tifs = list.files(imagery, pattern = "\\.tif")
rast_2014 <- raster(paste(imagery, "/", tifs[5], sep=""))
rast_2015 <- raster(paste(imagery, "/", tifs[16], sep=""))

# use world geodesic survey 1984 spatial coordinates
wgs84 <- "+proj=longlat +datum=WGS84 +ellps=WGS84 +towgs84=0,0,0"
projection(rast_2014) <- CRS(wgs84)
projection(rast_2015) <- CRS(wgs84)

# create a list of counties
# McKenzie County, ND and Williams County, ND don't work because they are cutoff in the satellite image
# counties <- c("Loving County, TX", "McKenzie County, ND", "Williams County, ND", "King County, TX")
counties <- c("Loving County, TX")

# set up graph display (no margins, one image)
par(mai=c(0,0,0,0),mfrow = c(1,1),bg='#001a4d', bty='n')

# plot light data for each county
for (i in 1:length(counties)){    
  # get bounds of city from google maps data
  temp_coord <- geocode(counties[i], source = "google")
  coords <- rbind(coords,temp_coord)
  
  e <- extent(temp_coord$lon - 1, temp_coord$lon + 1,
              temp_coord$lat - 0.25, temp_coord$lat + 0.25)
  rc <- crop(rast_2015, e)
  
  # calculate rescale brackets for quantiles
  num_quantiles = 10
  sampled <- as.vector(rc)
  sorted <- sort(sampled)
  
  quantile = c()
  # quantile[0] = 0
  quantile_labels = c()
  for (j in 1:num_quantiles){
    quantile[j] = sorted[ j / num_quantiles * length(sorted)]
    if (j == 1){
      indices <- which(sampled <= quantile[1])
      quantile_labels[indices] = 1
      #print('sasha')
    } else{
      #print(j)
      indices <- which(sampled <= quantile[j] & sampled > quantile[j-1])
      quantile_labels[indices] = j
    }
  }
    
  combined <- as.data.frame(cbind(sampled,quantile_labels))
  brk <- sort(aggregate(combined[,1], list(combined[,2]), max)[,2])
  
  # plot data
  plot(rc, breaks=brk, col=colorRampPalette(c("#001a4d","#0066FF", "yellow"))(num_quantiles), 
       legend=F,yaxt='n',xaxt='n',frame = F, asp=1.5)
  text(temp_coord$lon ,temp_coord$lat + 0.15,
       substr(counties[i],1,regexpr(",",counties[i])-1), 
       col="white", cex=1.25)
  
  rm(combined)
}