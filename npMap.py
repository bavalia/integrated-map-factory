#!/usr/bin/python3
"""
    #+brief : A subclass of numpy to store map with gps coordinates mapping
    #+author Kunal_Patel @ Swaayatt-Robots
    #+date 2017/oct/10
    #Earth Radius (R)    # 6371.3 Km           # 6371.3 [6349-6378]  km

#TODO
separare pure npMap functions and googleMaps
remove cv2 dependance
"""

### Includes ###
import numpy as np

### Default Parametes ###


### Constants ###
swytLocConst        = 0.0005            # deg
swytHeightConst     = 556               # pixels
swytLenghtConst     = 55.6              # meter
C_dist2lat          = swytLocConst/swytLenghtConst

def C_dist2lon(lat):
    return C_dist2lat/np.cos(lat/180*np.pi)

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
        #TODO # check why dist2row and dist2col are not equal!!??
              # Ans: height and width are trimmed to int, so not equal
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

    def isInside(self, gps):
        if len(gps) == 2 and np.shape(gps) == (2,):
            return gps[0]>self.latMin and gps[0]<self.latMax and \
                gps[1]>self.lonMin and gps[1]<self.lonMax
        else :
            return np.all([gps[:,0]>self.latMin, gps[:,0]<self.latMax, \
                        gps[:,1]>self.lonMin, gps[:,1]<self.lonMax], axis=0)
            # Slower than np
            # return [gp[0]>self.latMin and gp[0]<self.latMax and \
            #     gp[1]>self.lonMin and gp[1]<self.lonMax for gp in gps]



# ### Main Function, just for testing purpose only ### 

if __name__ == '__main__':

    from gpsTools import *
    npMap.testGpsTrace()
