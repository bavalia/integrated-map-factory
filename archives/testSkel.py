import numpy as np
from gpsTools import *
from mapGenerator import mapGenerator
from time import time
from mapFactory import *
import cv2


# #society (23.233815, 23.23552833, 77.48972833, 77.492635)
# latMin              = 23.233815
# latMax              = 23.23552833
# lonMin              = 77.48972833
# lonMax              = 77.492635

# delta = 0.0001
# img = maps((23.233815-delta, 23.23552833+delta, 77.48972833-delta, 77.492635+delta), None, None, "roadmap")
# cv2.imshow("img", img)
# cv2.waitKey(0)

# delta = 30  # meter
# mapType = 'roadmap'
# # size = (90,160)
# size = None

# # gps = gpsUnique(gpsLoad("society.txt"))
# # gps = gpsUnique(gpsLoad("u_turn.txt"))
# gps = gpsUnique(gpsLoad("../gps_world/gps_road/25_4_2017r.txt"))

# img = maps((latMin, latMax, lonMin, lonMax))
# img = fitScreen(img)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.imread("mapSocietySkel.png", 0)

cv2.imshow("img", img)
cv2.waitKey(0)

# skel = np.zeros_like(img)
# element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
# print (element.shape, element)

# done = False
# while not done:
#     eroded = cv2.erode(img, element)
#     cv2.imshow("img", eroded )
#     cv2.waitKey(0)
#     temp = cv2.dilate(eroded, element)
#     cv2.imshow("img", temp)
#     cv2.waitKey(0)
#     temp = img - temp
#     cv2.imshow("img", temp)
#     cv2.waitKey(0)
#     temp = cv2.bitwise_or(skel, temp)
#     cv2.imshow("img", temp)
#     cv2.waitKey(0)
#     img = eroded.copy()

    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # done = cv2.countNonZero(img)==0
