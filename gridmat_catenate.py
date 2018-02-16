import numpy as np
from optparse import OptionParser
import matplotlib.pyplot as plt
import os
import sys
import glob

thickness_files= glob.glob("./*average_thickness.dat")
data_thickness=np.array([])

for path in thickness_files:
    data_thickness=np.append(data_thickness, np.genfromtxt(path))

thick_av=np.average(data_thickness)*10
thick_sd=np.std(data_thickness)*10
print ("The averaged thickness is: "+str(round(thick_av,3)) + " +/- " + str(round(thick_sd,3))+ " Ang.")


top_area_files= glob.glob("./*top_areas.dat")
bot_area_files= glob.glob("./*bot_areas.dat")
data_area=np.array([])

for path in top_area_files:
    temp_file=np.genfromtxt(path, dtype="str", max_rows=1)
    val=float(temp_file[3])
    data_area=np.append(data_area, val)

for path in bot_area_files:
    temp_file=np.genfromtxt(path, dtype="str", max_rows=1)
    val=float(temp_file[3])
    data_area=np.append(data_area, val)

area_av=np.average(data_area)
area_sd=np.std(data_area)
print("The average area per lipid is: " + str(round(area_av,3)) + " +/- " + str(round(area_sd,3)) + " sqr. Ang.")
