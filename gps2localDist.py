import numpy as np
import os
from gpsTools import *

file = "society2018apr.txt"
name, ext = os.path.splitext(file)
outfile = name + "Local" + ext


gps = gpsLoad(file)

lon2dist = 1/C_dist2lon(gps[0,0]) # lon delta per unit distance at given lat
lat2dist = 1/C_dist2lat

local = gps - gps[0]
local[:,0] = local[:,0] * lat2dist
local[:,1] = local[:,1] * lon2dist

local = local[:,(1,0)]

np.savetxt(outfile, local, fmt="%0.3f")


################################################################################

# print for debugging
# print(local)
print( "local distance in meter is saved to : " + outfile)

xmax, ymax = np.max(local, 0)
xmin, ymin = np.min(local, 0)
print("x:", xmin, ",", xmax, "  y:", ymin, ",", ymax)

dist = np.sqrt(np.sum(local**2, 1).max())
print("Max Distance from start in Meters: ",dist)


# plot for evaluation of trajectory
import matplotlib.pyplot as plt

plt.scatter(local[:,0], local[:,1] )
plt.show()
