#!/usr/bin/python3
"""
    @brief Google Maps Calibration
    @author Kunal_Patel @ Swaayatt-Robots
    @date 2017/oct/11
"""
earthR = 6371.3
width = 640
height = 640

lonWidth = 373 #fixed, if even required 374
lonDelta = int((width-lonWidth)/2)
print (lonDelta)

import numpy as np
import cv2

file0 = "calibration_0.237.png"
file1 = "calibration_23.237.png"
file2 = "calibration_50.237.png"
file3 = "london_51.5074.png"

lat0 = 0.237
lat1 = 23.237
lat2 = 50.237
# lat3 = 51.5704
lat3 = 51.5074

latHeight = int(np.rint(lonWidth / np.cos(lat3/180*np.pi)))
latDelta = int((height-latHeight)/2)
print (latHeight)




### lat 0 ###
img = cv2.imread(file3)
print(file3, type(img))
img2 = img.copy()

img[:, lonDelta, ...] = 0 
img[:, lonDelta+lonWidth, ...] = 0 
img[[latDelta,latDelta+latHeight], ...] = 0

# img = np.hstack([img, img2])

# key = None
# while key is not 27 :
  # cv2.imshow("img", img)
  # key = cv2.waitKey(0)

for lat in range(90):
    latHeight1 = int(np.rint(lonWidth / np.cos(lat/180.*np.pi)))
    latDelta = ((height-latHeight1)/2)
    print (lat,latHeight1, int(latDelta), latDelta)

