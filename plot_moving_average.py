import numpy as np
from optparse import OptionParser
import matplotlib.pyplot as plt
import os
import sys

parser=OptionParser()
parser.add_option("-f", "--gro", action="store", type='string', dest="InputFile", default='data.dat', help="Name of the file with the data")
parser.add_option("-x", "--independent", action="store", type='int', dest="XColumn", default='0', help="Number of the column (starting on 0) to be plotted in the X axis")
parser.add_option("-y", "--dependent", action="store", type='int', dest="YColumn", default='1', help="Number of the column (starting on 0) to be plotted in the X axis")
parser.add_option("-o", "--out", action="store", type='string', dest="OutputFile", default='matrix.pdf', help="Name of the output image")
(options, args)= parser.parse_args()
inname_opt=options.InputFile
x_col=options.XColumn
y_col=options.YColumn
outname_opt=options.OutputFile
window=7500

def mov_average(data, N):
    cumsum, moving_aves = [0], []
    for i, x in enumerate(data, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)
    return moving_aves

inp=np.genfromtxt(inname_opt, skip_header=29)
x_dat=inp[:,x_col]
y_dat=inp[:,y_col]
print(np.shape(x_dat), np.shape(mov_average(y_dat,window)))
fig=plt.figure()
plt.title(inname_opt)
plt.plot(x_dat[window-1:], mov_average(y_dat,window))
plt.grid()
plt.savefig(outname_opt)
plt.close()
