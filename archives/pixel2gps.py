from mapFactory import *
import cv2


delta = 0.0001
img = maps((23.233815-delta, 23.23552833+delta, 77.48972833-delta, 77.492635+delta), None, None, "roadmap")
img2 = maps(img.mapRange, cv2.imread("mapSocietyBin.png"))
print(img2.shape, type(img2))


with open("societyGridLat.txt", 'w') as wLat:
    for y in range(img.shape[0]):
        wLat.write(str(img2.row2lat(y)) + "\n")

with open("societyGridLon.txt", 'w') as wLon:
    for x in range(img.shape[1]):
        wLon.write(str(img2.col2lon(x)) + "\n")

