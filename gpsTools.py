#!/usr/bin/python3
"""
    #+brief GPS formulas and file loading functions for swaayatt 
    #+author Kunal_Patel @ Swaayatt-Robots
    #+date 2017/oct/19

    #### frame work scale, z20
    0.000008993 deg = 1.0 m       = 10 pixels
    0.00001 deg     = 1.112 m     = 11.12 pixels
    0.0005 deg      = 55.6 m      = 556 pixels 
    0.001 deg       = 111.2 m     = 1112 pixels

#TODO
"""

### Includes ###
import numpy as np


### Constants ###
earthRadius         = 6371.3            # Km
swytLocConst        = 0.0005            # deg
swytHeightConst     = 556               # pixels
swytLenghtConst     = 55.6              # meter
C_dist2lat          = swytLocConst/swytLenghtConst

def C_dist2lon(lat):
    return C_dist2lat/np.cos(lat/180*np.pi)

### Function Definations ###

def gpsLoad(name):
    coordinates = np.loadtxt(name, usecols=(1,2), delimiter=',')
    return coordinates

def gpsLoggerLoad(name):
    coordinates = np.loadtxt(name, usecols=(2,3), delimiter=',', skiprows=1)
    return coordinates

def gpxLoad(name):
    import gpxpy
    with open(name, 'r') as gpxFile:
        gpx = gpxpy.parse(gpxFile)

    coordinates = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coordinates += [(point.latitude, point.longitude)]

    return np.array(coordinates)


def gpsUnique(coordinates):
    select = coordinates[:-1]!=coordinates[1:]
    select = select.any(axis=1)
    return  coordinates[np.hstack([[True], select])]


def main():
    # array = gpsLoad("gpsLoc/society.txt")
    array = gpsLoad("gpsLoc/17/17_10_2017_0.txt")
    uniq = gpsUnique(array)
    print (array.shape, uniq.shape)
    print(uniq[:20])
    print(uniq[-20:])


if __name__ == '__main__' : main()


