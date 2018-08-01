# integrated-map-factory
A full map solution for localization in self-driving cars with integrated coordinates-distance-pixel array of map, uses google maps for source

## Features of this project
* Python3 project with numpy library
* Low level APIs for support
  * [npMap](npMap.py) container as subclass of numpy array to store maps with coordinates-distance-pixel integration
    * latitude-hight(m)-rows(pixel) / longitude-width(m)-columns(pixel) conversion formulas as npMap attributes
  * mapDownloader to download patch of maps from google maps api
    * google API key can be integrated for heavy usage
    * type of maps satellite, mapsOnly, hybrid can be selected
    * zoom level of map can be selected, default zoom is 20 with maximum details-
  * mapGenerator to stitch patches of maps and prepare the map with given coordinate integration
    * integrates mapDownloader and npMap to generate maps 
    * integrates attibutes to given npMap and sets constants for conversion formula for the map
* High level APIs to build use cases
  * gpsTools to extract gps data from files and manupulate gps data
    * gpxLoad('gpx_file_name')  # to load gps data from gpx file
    * gpsLoggerLoad('fileName.txt') # gpsLogger file in txt form to be loaded
    * gpsLoad('filename.txt') # to load few of gps sample files given; with 1st col as lat, 2nd col as lon
    * gpsUnique(gps_data) #to filter out multiple continuous same entry
  * mapFactory to generate and manupulate maps
    * maps(maprange, obj=None, winSize=None, maptype='roadmap') #function to generate map with given range
    * maprange = (latmin,latmax,lonmin,lonmax) # always need to be defined
    * obj : any npMap or image need to be converted to map with given coordinate range    
    * winSize = (rows,cols) # output image size
    * maptype : roadmap/satellite/hybrid
  * movingCarWindow to show a realtime map with localization like navigation
    * just needs GPS stream of data and orientation for realtime map navigation
  
