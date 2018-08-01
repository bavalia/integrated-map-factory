# Google Maps API Guide

* Earth Radius (R)    # 6371.3 Km           # 6371.3 [6349-6378]  km
* angle in 1 Km at equator (1/R*180/pi)   # approx = 0.0090 deg   # 0.008993 deg = 0.000156954 rad
* distance in 1 degree at equator         # 111.19492664455875 Km

* 0.0005 deg      = 55.6 m
* 0.001 deg       = 111.2 m
* 0.00001 deg     = 1.112 m
* 0.000008993 deg = 1.0 m

# GPS
* gps accuracy        = upto 15 m 
* DGps accuracy       = upto 10 cm theoritically !! 
* http://www.ndblist.info/datamodes/worldDGPSdatabase.pdf
* Differential GPS accuracy               # 0.00000_166(1000/6) deg = 0.18532487774093124 m 
* 0.00001 deg         = 1.1119492664455875 m        = 1.112 m approx



# Google Maps APIs 

## Static Maps 
* httpis://developers.google.com/maps/documentation/static-maps/
* eg: https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=23.1957,77.5117&zoom=17&size=640x640&style=element:labels|visibility:off

### Static Maps APIs
* https://developers.google.com/maps/documentation/static-maps/intro

* https://maps.googleapis.com/maps/api/staticmap?   # base url
* &center=23.1957,77.5117                 # required
* &zoom=20                                # required
* &size=640x640                           # required max(640x640)
* &scale=2            # max (1280x1280)   # scales image 2 times 
* &style=element:labels|visibility:off    # remove labels
* &maptype=satellite                      # satellite/roadmap*/hybrid
* &path=weight:1|23.2509,77.5110|23.2499,77.5110|23.2499,77.5121
* &markers=color:red%7Clabel:C%7C23.2499,77.5110
* &key=YOUR_API_KEY                       # key, 25000 free images/day

## Zoom Level 
* each level doubles the scale

### 20Z 
#### Lon (mathematically varries with Lat, but fixed in googleMaps)
##### for all Lat
* 2 pixel error  = 0.00000268 deg error
* 0.00000134 deg = 1 pixel
* 0.0005 deg     = 373 pixels (374 for practical purposes if pixels need even)

#### Lat (mathematically fixed, but in google not fixed !! why??)
##### Lat 23.23
* 406 Lat pixels = (373 Lon pixels)/cos(23.23 deg Lat)
* 0.0005 deg     = 406 pixels   = 55.6 m approx
* 0.001 deg    = 812 pixels  = 111.2 m approx
* 0.00001 deg    = 8.12 pixels  = 1.112 m approx

### 19Z 
* 0.001 deg    = 406 pixels  = 111.2 m approx
* 0.00001 deg    = 4.06 pixels  = 1.112 m approx

### Zoom Level Ratios
* 20 : 1128.497220
* 19 : 2256.994440
* 18 : 4513.988880
* 17 : 9027.977761
* 16 : 18055.955520
* 15 : 36111.911040
* 14 : 72223.822090
* 13 : 144447.644200
* 12 : 288895.288400
* 11 : 577790.576700
* 10 : 1155581.153000
* 9  : 2311162.307000
* 8  : 4622324.614000
* 7  : 9244649.227000
* 6  : 18489298.450000
* 5  : 36978596.910000
* 4  : 73957193.820000
* 3  : 147914387.600000
* 2  : 295828775.300000
* 1  : 591657550.500000


# GPS_Image framework

## Architecture and Files

### Files
* 1. map Downloader and convert to swaayatt format
* 2. map generater for given lat-lon range and zoom range
* 3. map factory to create display object, which maintains dist-pixel-loc relation

* old_folder          # mapImages/19/406x406/map/23.250,77.511.png
* size                # [406x406/640x640/..]
* zoom                # [../18/19/20]
* center              # yy.yyy,xx.xxx     # map for each 0.001 delta

* swaayatt_folder     # mapSwaayatt/l50p556/roadmap/2325000,7751100.png
* scale               # location delta(10^5) = 50, image size = 556 pixels
* map                 # [roadmap/satellite/hybrid]
* swaayatt_center     # yyyyyyy,xxxxxxx # map for each delta (10^5)

## Fixed things
### Distance vs Pixels #TODO scale google image accordingly
#### frame work scale, z20
* 0.000008993 deg = 1.0 m       = 10 pixels
* 0.00001 deg     = 1.112 m     = 11.12 pixels
* 0.0005 deg      = 55.6 m      = 556 pixels 
* 0.001 deg       = 111.2 m     = 1112 pixels

at equator
#### 20z google
* 0.0005 deg     = 373 pixels   = 55.6 m 
* 0.001 deg      = 746 pixels   = 111.2 m
* 0.00001 deg    = 7.46 pixels  = 1.112 m


## Attached things
### Zoom Levels
#### 20z


