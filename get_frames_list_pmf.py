import numpy as np
from optparse import OptionParser
import os
import sys
import re

parser=OptionParser()
parser.add_option("-i", "--input", action="store", type='string', dest="Distances", default='NP-MEM_pullx.xvg', help=".xvg file with the time and distances printed by Gromacs")
parser.add_option("-d", "--delta", action="store", type='float', dest="Delta", default='0.14', help="Distance (nm) between the COMs differences between each frame")
parser.add_option("-o", "--output", action="store", type='string', dest="Output", default='frames2get', help="Output filename")
parser.add_option("-t", "--timelapse", action="store", type='float', dest="TimeLapse", default='1.0', help="Time between each frame (ps)")

(options, args)= parser.parse_args()

distances_opt=options.Distances
delta_opt=options.Delta
output_opt=options.Output
time_opt=options.TimeLapse

inp=np.genfromtxt(distances_opt, skip_header=16)
distances=inp[:,1]
times = inp[distances>=0.0, 0]
distances = distances[distances>=0.0]

distances = distances[times%time_opt==0]
times = times[times%time_opt==0]

dist_act=0.0
indexes=np.array([])
while dist_act <= distances[0]:
    temp=np.abs(distances-dist_act)
    indexes=np.append(indexes, np.where(temp==np.min(temp))[0][0])
    dist_act += delta_opt

out_file=open(output_opt+".dat", "w")
ndx_file=open(output_opt+".ndx", "w")
out_file.write("Time (ps) \t Ideal distance (nm) \t Closest frame \t Closest frame distance (nm) \t Frames new index\n")
ndx_file.write("[ Frames ]" + "\n")
for i in range(len(indexes)):
    time=times[int(indexes[i])]
    out_file.write("{:.2f}".format(time).ljust(17))
    ideal_dist=i*delta_opt
    out_file.write("{:.3f}".format(ideal_dist).ljust(24))
    frame=int(round(time/time_opt))
    out_file.write("{:.0f}".format(frame).ljust(16))
    closest_dist=float(distances[np.where(times==frame*time_opt)])
    out_file.write("{:.3f}".format(closest_dist).ljust(32))

    out_file.write("{}".format(len(indexes)-i-1) + "\n")

    ndx_file.write("{:.0f}".format(frame) + "\n")

out_file.close()
ndx_file.close()
