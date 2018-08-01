#!/usr/bin/python3
"""
    @brief Google Maps Stitcher
    @author Kunal_Patel @ Swaayatt-Robots
    @date 2017/oct/10
#TODO
1. Map Joining Width of all maps should be same
2. Cached Maps, for faster loading
3. Set zoom level, delta, image size # automate it
4. Generate Map for bigger size using smaller size maps
"""

### Includes ###
import os
import numpy as np
import cv2
from mapDownloader import swaayattMapDownloader as SMD

### Default Parametes ###

C_delta               = 0.0005
zoom                = 20
# zoom                = 18

# maptype             = 'satellite'
maptype             = 'roadmap'
# maptype             = 'hybrid'

# # Center
# delt = 0.0005
# Lat , Lon = 23.234, 77.49
# latMin  = Lat - delt
# latMax = Lat + delt
# lonMin = Lon - delt
# lonMax = Lon + delt

# latMin              = 23.233815
# latMax              = 23.23552833
# lonMin              = 77.48972833
# lonMax              = 77.492635

# #society (23.233815, 23.23552833, 77.48972833, 77.492635)
# latMin              = 23.233815
# latMax              = 23.23552833
# lonMin              = 77.48972833
# lonMax              = 77.492635

#road - u_turn (23.192695, 23.198698, 77.511206, 77.512173)
latMin              = 23.192695
latMax              = 23.198698
lonMin              = 77.511206
lonMax              = 77.512173

# #road - full 
# latMin              = 23.1478733
# latMax              = 23.23713
# lonMin              = 77.4945366
# lonMax              = 77.515238

### Constants ###
precision           = 5
swytHeightConst     = 556               #pixels
tensFactor          = 10**precision
#TODO what if image size is different than p556
imgBaseFolder       = "./mapSwaayatt/"



def mapGenerator(latMin, latMax, lonMin, lonMax, maptype='roadmap', zoom=20, delta=None):

    delta = 2**(20-zoom) * C_delta
    if maptype not in ["roadmap", "satellite", "hybrid"] :
        maptype = "roadmap"
    imgFolder = imgBaseFolder + \
                "l" + str(int(delta *tensFactor)) +"p556/" + \
                maptype + "/"

    smd = SMD(maptype, delta, zoom)

    _delta = int(delta * tensFactor)
    _latMin    = int(np.rint(latMin * tensFactor /_delta)) *_delta
    _latMax    = int(np.rint(latMax * tensFactor /_delta)) *_delta
    _lonMin    = int(np.rint(lonMin * tensFactor /_delta)) *_delta
    _lonMax    = int(np.rint(lonMax * tensFactor /_delta)) *_delta
    nLat      = int((_latMax-_latMin)/_delta) + 1
    nLon      = int((_lonMax-_lonMin)/_delta) + 1
    print(_latMin, _latMax, _lonMin, _lonMax, nLat,"*", nLon,"=", nLat*nLon)

    # imgUnion  = np.zeros((imgSizeHeight * nLatDelta, imgSizeWidth * nLonDelta, 3), dtype=np.uint8 )

    ### map joining #TODO width of all images should be same for joining
    vstack = None
    for iLat in range(nLat):
        hstack = None
        for iLon in range(nLon):
            _lat = _latMin + iLat * _delta
            _lon = _lonMin + iLon * _delta
            imgTitle = str(_lat) + "," + str(_lon) + ".png"

            img = cv2.imread(imgFolder + imgTitle)
            if img is None :
                smd.getSwaayattMap(_lat/tensFactor, _lon/tensFactor)
                img = cv2.imread(imgFolder + imgTitle)
            if img is None:
                print ("ERROR: img is none", imgFolder + imgTitle)
            # cv2.imshow("img", img)
            # cv2.waitKey(0)

            if hstack is not None:
                hstack = np.hstack([hstack, img])
            else :
                hstack = img

        if vstack is not None:
            vstack = np.vstack([hstack, vstack])
        else :
            vstack = hstack


    ### map trimming upto required boundary
    lat2pix = swytHeightConst/delta
    lon2pix = int(np.rint(lat2pix * np.cos(_latMin/tensFactor/180*np.pi)))

    trimLeft = int(np.rint((lonMin -(_lonMin/tensFactor -delta/2))*lon2pix))
    trimTop  = int(np.rint((_latMax/tensFactor +delta/2 - latMax)*lat2pix))
    imgWidth  = int(np.rint((lonMax-lonMin)*lon2pix))
    imgHeight = int(np.rint((latMax-latMin)*lat2pix))

    vstack = vstack[trimTop: trimTop+imgHeight, trimLeft: trimLeft+imgWidth]

    return vstack


if __name__ == '__main__':

    vstack = mapGenerator(latMin, latMax, lonMin, lonMax, maptype, zoom)

    print(vstack.shape)
    y,x = vstack.shape[0:2]
    ymax, xmax = 700, 1300
    factor = np.max([y/ymax, x/xmax])
    y,x = int(y/factor), int(x/factor)
    imgUnion = cv2.resize(vstack, (x,y))
    print(imgUnion.shape)


    key = None
    while key is not 27 :
      cv2.imshow("imgUnion", imgUnion)
      key = cv2.waitKey(0)
