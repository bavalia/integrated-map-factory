#!/usr/bin/python3
"""
    #+brief Google Maps Stitcher
    #+author Kunal_Patel @ Swaayatt-Robots
    #+date 2017/oct/10

    #### frame work scale, z20
    0.000008993 deg = 1.0 m       = 10 pixels
    0.00001 deg     = 1.112 m     = 11.12 pixels
    0.0005 deg      = 55.6 m      = 556 pixels 
    0.001 deg       = 111.2 m     = 1112 pixels

#TODO
1. Map Scale, Convert zoom number to other parameter like delta
"""

### Includes ###
import os
import numpy as np
import cv2
from mapGenerator import mapGenerator

### Default Parametes ###


### Constants ###
swytLocConst        = 0.0005            # deg
swytHeightConst     = 556               # pixels
swytLenghtConst     = 55.6              # meter


### Class Definations ###

class npMap(np.ndarray):
    # Reference:https://docs.scipy.org/doc/numpy/user/basics.subclassing.html

    def __new__(subtype, obj, mapRange):
        '''
        # mapRange = tuple (latMin, latMax, lonMin, lonMax)
        # obj = numpy like ndarray
        '''
        # print ("in __new__")
        npMap.checkParameters(obj, mapRange)

        mapObj = obj.view(npMap)           # View ndarray as npMap class
        mapObj.setRange(mapRange)
        # print(type(mapObj), mapObj.shape)

        return mapObj

    def __array_finalize__(self, obj):
        # print("in __array_finalize__")
        if obj is None : return
        # print(type(self), self.shape, type(obj), obj.shape)
        # print( getattr(self,'latMin',"None"), getattr(obj,'latMin',"None"))

        if self.shape == obj.shape and \
           getattr(obj, "mapRange", None) is not None:
            self.copyParameters(obj)

    def checkParameters(obj, mapRange):
        if obj is None :
            raise (TypeError("object given is None"))
        if mapRange is None or len(mapRange) is not 4:
            raise (TypeError("mapRange should be in the form (latMin, latMax, lonMin, lonMax) "))


    def setRange(self, mapRange):
        #TODO make private
        self.mapRange = mapRange
        self.latMin  = mapRange[0]
        self.latMax  = mapRange[1]
        self.lonMin  = mapRange[2]
        self.lonMax  = mapRange[3]
        self.setParameters()

    def setParameters(self):
        #TODO set distance parameters, lat2dist, lon2dist, pix2dist
        #TODO #TOCHECK Reliable upto 8-10 digits
        height, width  = self.shape[:2]
        latSize      = self.latMax - self.latMin
        lonSize      = self.lonMax - self.lonMin
        self.C_lat2row  = height / latSize
        self.C_lon2col  = width  / lonSize
        self.C_lat2dist = swytLenghtConst / swytLocConst
        self.C_lon2dist = self.C_lat2dist * np.cos(self.latMin/180*np.pi)
        self.C_dist2row = self.C_lat2row / self.C_lat2dist
        self.C_dist2col = self.C_lon2col / self.C_lon2dist

    def copyParameters(self, obj):
        self.mapRange         = obj.mapRange
        self.latMin           = obj.latMin
        self.latMax           = obj.latMax
        self.lonMin           = obj.lonMin
        self.lonMax           = obj.lonMax
        self.C_lat2row        = obj.C_lat2row
        self.C_lon2col        = obj.C_lon2col
        self.C_lat2dist       = obj.C_lat2dist
        self.C_lon2dist       = obj.C_lon2dist
        self.C_dist2row       = obj.C_dist2row
        self.C_dist2col       = obj.C_dist2col

    ### uncomment if needed
    def lat2row(self, lat):
        return int(np.rint((self.latMax - lat) * self.C_lat2row))

    def row2lat(self, row):
        return (self.latMax - row / self.C_lat2row)

    def lon2col(self, lon):
        return int(np.rint((lon - self.lonMin) * self.C_lon2col))

    def col2lon(self, col):
        return (self.lonMin + col / self.C_lon2col)

    def gps2pix(self, gps):
        ''' gps:(lat, lon), pix:(row, col) '''
        return ( int(np.rint((self.latMax - gps[0]) * self.C_lat2row)) , \
                 int(np.rint((gps[1] - self.lonMin) * self.C_lon2col)) )

    def pix2gps(self, pix):
        return ( self.latMax - pix[0] / self.C_lat2row , \
                 self.lonMin + pix[1] / self.C_lon2col )

    def slicePix(self, pixRange):
        obj = self[pixRange[0]:pixRange[1], pixRange[2]:pixRange[3] ]
        obj.setRange((self.row2lat(pixRange[1]), self.row2lat(pixRange[0]), \
                      self.col2lon(pixRange[2]), self.col2lon(pixRange[3])))
        return obj

    def sliceLoc(self, mapRange):
        obj = self[self.lat2row(mapRange[1]): self.lat2row(mapRange[0]), \
                   self.lon2col(mapRange[2]): self.lon2col(mapRange[3]) ]
        obj.setRange(mapRange)
        return obj

    def gpsMarks(self, gpsPoints, color=(0,0,255), radius=3):
        if len(gpsPoints) == 2 and np.shape(gpsPoints) == np.shape((1,1)):
            cv2.circle(self, self.gps2pix(gpsPoints)[::-1], radius, color)
        else :
            for point in gpsPoints :
                cv2.circle(self, self.gps2pix(point)[::-1], radius, color)

    def gpsPath(self, gpsPath, color=(0,0,255)):
        #TODO : optimize the routine, checks are twice now
        #TODO : paremeters ==> line width, line color
        prev = gpsPath[0]
        for loc in gpsPath[1:]:
            if (loc[0]<= self.latMax and  \
                loc[0]>  self.latMin and  \
                loc[1]>= self.lonMin and  \
                loc[1]<  self.lonMax) or  \
               (prev[0]<= self.latMax and \
                prev[0]>  self.latMin and \
                prev[1]>= self.lonMin and \
                prev[1]<  self.lonMax) :
                cv2.line(self, self.gps2pix(prev)[::-1], self.gps2pix(loc)[::-1], color)
            prev = loc

    def fitScreen(self):
        y,x = self.shape[0:2]
        ymax, xmax = 700, 1300
        factor = np.max([y/ymax, x/xmax])
        y,x = int(y/factor), int(x/factor)
        return maps(self.mapRange, self, (y,x))


    def testGpsTrace():
        delta = 0.0001
        deltah = delta * 0
        deltav = delta * -20
        map1 = maps((23.233815-delta, 23.23552833+delta, 77.48972833-delta, 77.492635+delta), None, None, "roadmap").fitScreen()
        # map1 = maps((23.192695-deltav, 23.198698+deltav, 77.511206-deltah, 77.512173+deltah), None, None, "hybrid")
        map1 = map1.fitScreen()
        # gps = gpsUnique(gpsLoad("society.txt"))
        # # map1.gpsMarks(gps)
        # map1.gpsPath(gps, (255,0,0))
        # map1.gpsMarks(gps[0], (0,255,0), 5)
        # map1.gpsMarks(gps[-1], (0,0,255), 5)
        # for i in range(10):
        #     print(i)
        #     gps = gpsUnique(gpsLoad("gpsLoc/17/17_10_2017_" +str(i) +".txt"))
        #     map1.gpsPath(gps, (0,255,0))
        # for i in range(7):
        #     print(i)
        #     gps = gpsUnique(gpsLoad("gpsLoc/18/18_10_2017_" +str(i) +".txt"))
        #     map1.gpsPath(gps)
        # map1.gpsMarks((23.234717, 77.492045), radius=0)
        # map1.gpsMarks((23.234701, 77.491746))
        # cv2.imshow("img", map1)
        # cv2.waitKey(0)
        cv2.imwrite("mapSociety.png", map1)

    def testFindRoad():
        delta = 0.0001
        map1 = maps((23.233815-delta, 23.23552833+delta, 77.48972833-delta, 77.492635+delta), None, None, "roadmap")
        # map1 = maps((23.192695-deltav, 23.198698+deltav, 77.511206-deltah, 77.512173+deltah), None, None, "hybrid")
        map1 = map1.fitScreen()
        road = cv2.Canny(map1, 10, 20)
        cv2.namedWindow("img")
        # cv2.imshow("img", roaD)
        cv2.imshow("img", map1)
        cv2.waitKey(0)
        # cv2.imwrite("mapRoad.png", map1)


    def testNpMap():
        print("in npMap test")
        map1 = maps((23.233815, 23.23552833, 77.48972833, 77.492635), None, (400, 600), "roadmap")
        map2 = map1.copy()
        map3 = map1.slicePix((2,10, 0, map1.shape[1])) #map1[2:10]
        print ((map1.row2lat(10), map1.row2lat(2), map1.lonMin, map1.lonMax))
        print (map3.mapRange)

        print (map1.shape, map1.C_dist2row, map1.C_dist2col, map1.C_lat2row)
        print (map2.shape, map2.C_dist2row, map2.C_dist2col, map2.C_lat2row)
        print (map3.shape, map3.C_dist2row, map3.C_dist2col, map3.C_lat2row)
        print (8/(map3.latMax-map3.latMin), map3.C_lat2row)

        print(map1.shape, map1.latMax, map1.mapRange)
        print(map1.gps2pix(map1.pix2gps(np.array(map1.shape[:2])/2)))
        print(map1.gps2pix((map1.latMin, map1.lonMax)))


### Function Definations ###

def maps(mapRange, obj=None, winSize=None, maptype='roadmap'):
    '''
    # mapRange = tuple (latMin, latMax, lonMin, lonMax)
    # obj      = any image or npMap, should be compatible with openCV
    # winSize  = tuple (rows, cols)
    # maptype  = roadmap/satellite/hybrid
    '''
    checkParameters(winSize=winSize, maptype=maptype)

    if obj is None:
        obj = mapGenerator(mapRange[0], mapRange[1], mapRange[2], mapRange[3], maptype)
        if obj is None:
            raise(ValueError("Image not found"))

    if winSize is not None:
        obj = cv2.resize(obj, winSize[::-1])  #size need in (width,heght)

    return npMap(obj, mapRange)


def checkParameters(mapRange=None, obj=None, winSize=None, maptype=None):
    #TODO more strict parameters checking
    #TODO obj checking

    if mapRange is not None and len(mapRange) is not 4:
        raise(TypeError("mapRange should be in the form (latMin, latMax, lonMin, lonMax) "))
    if winSize is not None and len(winSize) is not 2:
        raise(TypeError("winSize should be in the form (width, height) in pixels"))
    if maptype is not None and maptype not in ["roadmap", "satellite", "hybrid"] :
        raise(ValueError('maptype should be one of "roadmap", "satellite", "hybrid"'))
    pass



### Main Function, just for testing purpose only ### 

if __name__ == '__main__':

    from gpsTools import *
    npMap.testGpsTrace()
