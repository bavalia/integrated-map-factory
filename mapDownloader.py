#!/usr/bin/python3
"""
    @brief Google Maps Downloader for Swaayatt
    @author Kunal_Patel @ Swaayatt-Robots
    @date 2017/oct/11

    # GPS_Image framework
    old_folder          # mapImages/19/406x406/map/23.250,77.511.png
    size                # [406x406/640x640/..]
    zoom                # [../18/19/20]
    center              # yy.yyy,xx.xxx     # map for each 0.001 delta

    swaayatt_folder     # mapSwaayatt/l50p556/roadmap/2325000,7751100.png
    scale               # location delta(10^5) = 50, image size = 556 pixels
    map                 # [roadmap/satellite/hybrid]
    swaayatt_center     # yyyyyyy,xxxxxxx # map for each delta (10^5)

    ## Fixed things
    ### Distance vs Pixels #TODO scale google image accordingly
    #### frame work scale, z20
    0.000008993 deg = 1.0 m       = 10 pixels
    0.00001 deg     = 1.112 m     = 11.12 pixels
    0.0005 deg      = 55.6 m      = 556 pixels
    0.001 deg       = 111.2 m     = 1112 pixels

    at equator
    #### 20z google
    0.0005 deg     = 373 pixels   = 55.6 m
    0.001 deg      = 746 pixels   = 111.2 m
    0.00001 deg    = 7.46 pixels  = 1.112 m

### #TODO #TODecide
# which size to use default ? 556 pixels-0.0005 deg or 1112 pixes-0.001 deg
Ans: Right now 556 pixes, as no need for process

# works upto 50 deg lattitude,
as image required for delta=50 jump is greater than 640 pixels on googleMaps
need to decrease the jump delta=25 for 54-73 deg lattitude
"""

### Includes ###

# import urllib                         # for python2
from urllib import request as urllib    # for python3
import os
import numpy as np
import cv2

### Default Parametes ###
latMin              = 23.23373
latMax              = 23.23565
lonMin              = 77.48954
lonMax              = 77.49273

# maptype             = 'satellite'
maptype             = 'roadmap'
# maptype             = 'hybrid'

# Other Default Parameters used, to change edit main function
zoom                = 20
delta               = 0.0005
precision           = 5
swytHeight          =  556
googleWidth         =  373
key                 = None
googleBaseFolder    = "./mapImages/"
swaayattBaseFolder  = "./mapSwaayatt/"

class googleMapDownloader:
    #TODO Class name should start with capital
    def __init__(self, zoom=16, sizeWidth=640, sizeHeight=640, maptype='roadmap', labels=False, scale=1, otherDefault=None, key=None):
        self._zoom            = zoom
        self._size            = str(sizeWidth) + "x" + str(sizeHeight)
        self._maptype         = maptype
        self._labels          = labels
        self._scale           = scale
        self._otherDefault    = otherDefault
        self._key             = key
        self._baseURL         = 'https://maps.googleapis.com/maps/api/staticmap?'
        self._queryDefault    = self.generateQueryDefault()

    def generateQueryDefault(self):
        queryDefault    = self._baseURL + \
                                "zoom=" + str(self._zoom) + \
                                "&size=" + self._size
        if self._maptype is not None:
            queryDefault += "&maptype=" + self._maptype
        if self._labels is False :
            queryDefault += "&style=element:labels|visibility:off"
        if self._scale is not None:
            queryDefault += "&scale=" + str(self._scale)
        if self._otherDefault is not None:
            queryDefault += self._otherDefault
        if self._key is not None:
            queryDefault += "&key=" + self._key

        return queryDefault

    def getImage(self, lat, lon, otherPara=None, title=None):

        url = self._queryDefault + "&center=" + str(lat) + "," + str(lon)

        if otherPara is not None:
            url += otherPara
        print (url, title)

        if title is not None:
            urllib.urlretrieve(url, title)
        else :
            urllib.urlretrieve(url, "tempImage.png")
            # print("Warning: image title not given, storred in 'tempImage.png'")
            img = cv2.imread("tempImage.png")
            return img

        return None

class swaayattMapDownloader(googleMapDownloader):

    def __init__(self, maptype='roadmap', delta=0.0005, zoom=20,  \
                 other=None, key=None, precision=5):
        self._precision       = precision
        self._tens            = 10**precision
        self._delta           = int(delta * self._tens)
        self._swytHeightConst = 556
        self._googleWidthConst= 373
        self._earthRadius     = 6371.3
        self._googleMaxSize   = 640

        scale            = 2       # googleImage clearity
        labels           = False
        portionOfImage   = int(2**(20-zoom) * 0.0005/delta)
        self._outHeight  = int(np.rint(self._swytHeightConst / portionOfImage))
        self._googleWidth= int(np.rint(self._googleWidthConst * scale / portionOfImage))
        # googleMapDownloader.__init__(zoom, self._googleMaxSize, \
        super().__init__(zoom, self._googleMaxSize, \
                                     self._googleMaxSize, maptype, \
                                     labels, scale, other, key)

        self._googleFolder    = "./mapImages/" + \
                                str(self._zoom) + "z" + \
                                str(self._scale) + "s""/" + \
                                self._size + "/" + \
                                self._maptype + "/"

        self._swaayattFolder  = "./mapSwaayatt/" + \
                                "l" + str(self._delta) + \
                                "p" + str(self._outHeight) + "/" + \
                                self._maptype + "/"

        if not os.path.exists(self._googleFolder):
            os.makedirs(self._googleFolder)
        if not os.path.exists(self._swaayattFolder):
            os.makedirs(self._swaayattFolder)


    def getSwaayattMap(self, lat, lon, otherPara=None):
        latRadiusFactor = np.cos(lat/180*np.pi)
        outWidth        = int(np.rint(self._outHeight * latRadiusFactor))
        googleHeight    = int(np.rint(self._googleWidth / latRadiusFactor))
        imgTitle = str(int(np.rint(lat * self._tens))) + "," + \
                   str(int(np.rint(lon * self._tens))) + ".png"

        img = cv2.imread(self._googleFolder + imgTitle)
        if img is None:
            self.getImage(lat, lon, otherPara, self._googleFolder + imgTitle)
            img = cv2.imread(self._googleFolder + imgTitle)
        if img is None:
            print ("ERROR: could not retrieve Google image:")
            print (self._googleFolder + imgTitle)
            exit(1)

        # left-top included, right-bottom excluded, as floored to int
        cutLeft  = int((img.shape[0] - self._googleWidth)/2)
        cutTop = int((img.shape[1] - googleHeight)/2)
        img = img[cutTop : cutTop + googleHeight, \
                  cutLeft : cutLeft + self._googleWidth]
        img = cv2.resize(img, (outWidth, self._outHeight))
        cv2.imwrite(self._swaayattFolder + imgTitle, img )
        print("Written: " + self._swaayattFolder + imgTitle)


    def getSwaayattMapRange(self, latMin, latMax, lonMin, lonMax):
        delta     = self._delta
        latMin    = int(np.rint(latMin * self._tens /delta)) *delta
        latMax    = int(np.rint(latMax * self._tens /delta)) *delta
        lonMin    = int(np.rint(lonMin * self._tens /delta)) *delta
        lonMax    = int(np.rint(lonMax * self._tens /delta)) *delta
        nLat      = int((latMax-latMin)/delta) + 1    # +1 for end images
        nLon      = int((lonMax-lonMin)/delta) + 1
        print(latMin, latMax, lonMin, lonMax, nLat,"*", nLon,"=", nLat*nLon)

        for iLat in range(nLat):
            for iLon in range(nLon):
                lat = (latMin + iLat * delta)/self._tens
                lon = (lonMin + iLon * delta)/self._tens
                self.getSwaayattMap(lat, lon)

if __name__ == '__main__':

    smd = swaayattMapDownloader(maptype)

    smd.getSwaayattMapRange(latMin, latMax, lonMin, lonMax)
