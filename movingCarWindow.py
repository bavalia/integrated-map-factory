import numpy as np
from gpsTools import *
from mapGenerator import mapGenerator
from time import time
from mapFactory import *
import cv2


delta = 30  # meter
mapType = 'roadmap'
# size = (90,160)
size = None

# gps = gpsUnique(gpsLoad("gpsLoc/society.txt"))
gps = gpsUnique(gpsLoad("gpsLoc/societyShort.txt"))
# gps = gpsUnique(gpsLoggerLoad("gpsLoc/gpsLogger.log"))
# gps = gpsUnique(gpsLoad("gpsLoc/u_turn.txt"))
# gps = gpsUnique(gpsLoad("../gps_world/gps_road/25_4_2017r.txt"))
# gps = gpsUnique(gpxLoad('gpsLoc/gpxTest.gpx'))


t = time()

# latDelta = delta * C_dist2lat
# lonDelta = delta * C_dist2lon(gps[0,0])
cv2.namedWindow("img")
gpsLen = len(gps)
for i, pt in enumerate(gps):
    # img = mapGenerator(pt[0]-latDelta, pt[0]+latDelta, pt[1]-lonDelta, pt[1]+lonDelta, mapType)
    # img = maps((pt[0]-latDelta*1/2, pt[0]+latDelta*3/2, pt[1]-lonDelta, pt[1]+lonDelta), None, size, mapType)
    top = min(i+3, gpsLen-1)
    bot = max(0, i-2)
    direction = np.arctan2(*(gps[top]-gps[bot]))
    img = mapRot(pt, direction, 50, 20, 25)

    # img = fitScreen(img)
    print("done till ", i, " out of ", len(gps))
    cv2.imshow("img", img)
    cv2.waitKey(1)

delay = time()-t
print("delay in sec= ", delay)
print("per image time= ", delay/len(gps), len(gps)/delay, "Hz")
