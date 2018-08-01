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
import numpy as np
import cv2
import npMap
from mapGenerator import mapGenerator

### Default Parametes ###


### Constants ###
swytLocConst        = 0.0005            # deg
swytHeightConst     = 556               # pixels
swytLenghtConst     = 55.6              # meter


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

    return npMap.npMap(obj, mapRange)

def mapRot(center, directionPi, frontMeter, backMeter, sideMeter, maptype='roadmap'):
    rotAngle = np.pi/2 - directionPi
    deltaMax = np.sqrt(max(frontMeter, backMeter)**2 + sideMeter**2)
    deltaLat = deltaMax * npMap.C_dist2lat
    deltaLon = deltaMax * npMap.C_dist2lon(center[0])
    img = maps((center[0]-deltaLat, center[0]+deltaLat, \
                center[1]-deltaLon, center[1]+deltaLon), maptype=maptype)
    gpsMarks(img, center)
    centRow = img.lat2row(center[0])
    centCol = img.lon2col(center[1])
    M = cv2.getRotationMatrix2D((centCol, centRow), rotAngle/np.pi*180, 1)
    imgRot = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]))
    xScale = np.sqrt((img.C_dist2col*np.cos(rotAngle))**2 + \
                     (img.C_dist2row*np.sin(rotAngle))**2)
    yScale = np.sqrt((img.C_dist2row*np.cos(rotAngle))**2 + \
                     (img.C_dist2col*np.sin(rotAngle))**2)
    # print (img.C_dist2row, img.C_dist2col)
    # print (yScale, xScale)
    xpix = int(np.rint(sideMeter*xScale))
    return imgRot[centRow-int(np.rint(frontMeter*yScale)) : \
                    centRow+int(np.rint(backMeter*yScale))  , \
                    centCol-xpix : centCol+xpix]

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


def gpsMarks(obj, gpsPoints, color=(0,0,255), radius=3):
    if len(gpsPoints) == 2 and np.shape(gpsPoints) == (2,):
        cv2.circle(obj, obj.gps2pix(gpsPoints)[::-1], radius, color)
    else :
        for point in gpsPoints :
            cv2.circle(obj, obj.gps2pix(point)[::-1], radius, color)

def gpsPath(obj, gpsPoints, color=(0,0,255)):
    #TODO : optimize the routine, checks are twice now
    #TODO : paremeters ==> line width, line color
    prev = gpsPoints[0]
    for loc in gpsPoints[1:]:
        if (loc[0]<= obj.latMax and  \
            loc[0]>  obj.latMin and  \
            loc[1]>= obj.lonMin and  \
            loc[1]<  obj.lonMax) or  \
            (prev[0]<= obj.latMax and \
            prev[0]>  obj.latMin and \
            prev[1]>= obj.lonMin and \
            prev[1]<  obj.lonMax) :
            cv2.line(obj, obj.gps2pix(prev)[::-1], obj.gps2pix(loc)[::-1], color)
        prev = loc

# def gpsPath(obj, gpsPath, color=(0,0,255)):
#     # slower than individual checks
#     #TODO : paremeters ==> line width, line color
#     inside = obj.isInside(gpsPath)
#     prev = gpsPath[0]
#     for i, loc in enumerate(gpsPath[1:]):
#         if inside[i+1] and inside[i]:
#             cv2.line(obj, obj.gps2pix(prev)[::-1], obj.gps2pix(loc)[::-1], color)
#         prev = loc

def fitScreen(obj):
    y,x = obj.shape[0:2]
    ymax, xmax = 700, 1300
    factor = np.max([y/ymax, x/xmax])
    y,x = int(y/factor), int(x/factor)
    return maps(obj.mapRange, obj, (y,x))

#############################   Testing Functions   ############################

def testGpsTrace():
    delta = 0.0001
    gps = gpsUnique(gpsLoad("society2018apr.txt"))
    # gps = gpsUnique(gpsLoad("society.txt"))
    # gps = gpxLoad("gpxTest.gpx")
    xmin = np.min(gps[:,1])-delta
    xmax = np.max(gps[:,1])+delta
    ymin = np.min(gps[:,0])-delta
    ymax = np.max(gps[:,0])+delta
    map1 = maps((ymin,ymax, xmin, xmax))
    map1 = fitScreen(map1)
    gpsPath(map1, gps, (255,0,0))
    gpsMarks(map1, gps[0], (0,255,0), 5)
    gpsMarks(map1, gps[-1], (0,0,255), 5)
    cv2.imshow("img", map1)
    cv2.waitKey(0)

def testGpsTraceSWT():
    delta = 0.0001
    deltah = delta * 0
    deltav = delta * -20
    map1 = maps((23.233815-delta, 23.23552833+delta, 77.48972833-delta, 77.492635+delta), None, None, "roadmap")
    map1 = fitScreen(map1)
    # map1 = maps((23.192695-deltav, 23.198698+deltav, 77.511206-deltah, 77.512173+deltah), None, None, "hybrid")
    map1 = fitScreen(map1)
    # gps = gpsUnique(gpsLoad("society.txt"))
    gps = gpsUnique(gpsLoad("society2018apr.txt"))
    # # map1.gpsMarks(gps)
    gpsPath(map1, gps, (255,0,0))
    gpsMarks(map1, gps[0], (0,255,0), 5)
    gpsMarks(map1, gps[-1], (0,0,255), 5)
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
    cv2.imshow("img", map1)
    cv2.waitKey(0)
    # cv2.imwrite("mapSociety.png", map1)

def testFindRoad():
    delta = 0.0001
    map1 = maps((23.233815-delta, 23.23552833+delta, 77.48972833-delta, 77.492635+delta), None, None, "roadmap")
    # map1 = maps((23.192695-deltav, 23.198698+deltav, 77.511206-deltah, 77.512173+deltah), None, None, "hybrid")
    map1 = fitScreen(map1)
    canny = cv2.Canny(map1, 10, 20)
    cv2.namedWindow("img")
    # cv2.imshow("img", canny)
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




### Main Function, just for testing purpose only ###

if __name__ == '__main__':

    from gpsTools import *
    # testGpsTraceSWT()
    testGpsTrace()
    # testFindRoad()
