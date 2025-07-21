#!/usr/bin/python3
"""
    @brief Google Maps Downloader
    @author Kunal_Patel @ Swaayatt-Robots
    @date 2017/oct/09
"""

# Default Parametes ###
zoom                = 20
precision           = 4
latMin              = int( 23.2335 * 10**precision )
latMax              = int( 23.2356 * 10**precision )
latDelta            = int(  0.0005 * 10**precision )
lonMin              = int( 77.4895 * 10**precision )
lonMax              = int( 77.4925 * 10**precision )
lonDelta            = int(  0.0005 * 10**precision )
imgSizeWidth        =  406
imgSizeHeight       =  406
key                 = None
imgBaseFolder       = "./mapImages/"

# maptype             = 'satellite'
maptype             = 'roadmap'


# import urllib                         # for python2
from urllib import request as urllib    # for python3 
from PIL import Image                   # to open saved image
import os

class googleMapDownloader:

    def __init__(self, zoom=16, sizeWidth=640, sizeHeight=640, maptype='roadmap', labels=False, scale=1, otherDefault=None, key=key):
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
            img = Image.open("tempImage.png")
            return img

        return None


if __name__ == '__main__':

    gmd = googleMapDownloader(zoom, imgSizeWidth, imgSizeHeight, maptype, key=key)

    imgFolder = imgBaseFolder + \
                str(gmd._zoom) + "/" + \
                gmd._size + "/" + \
                gmd._maptype + "/"

    if not os.path.exists(imgFolder):
        print("The " , imgFolder , " directory does not exist, created it") 
        os.makedirs(imgFolder)

    lat, lon = latMin, lonMin
    while lat <= latMax:
        while lon <= lonMax:
            sLat = ("%." + str(precision) + "f") %(lat/(10**precision))
            sLon = ("%." + str(precision) + "f") %(lon/(10**precision))
            imgTitle = sLat + "," + sLon + ".png"
            gmd.getImage(sLat, sLon, None, imgFolder+imgTitle)
            lon += lonDelta
        lat += latDelta
        lon = lonMin



