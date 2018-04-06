import numpy as np
from optparse import OptionParser
import os
import sys
import scipy.constants as const

parser=OptionParser()
parser.add_option("-f", "--input", action="store", type='string', dest="MetricFile", default='Metrics.xvg', help="Column file with the box length in X and Y")
parser.add_option("-o", "--output", action="store", type='string', dest="OutputFile", default='Compressibility.log', help="Name of the output file")
parser.add_option("-x", "--xcol", action="store", type='int', dest="Box_X_Col", default='0', help="Number of the column (starting in 0) with the X length of the box")
parser.add_option("-y", "--ycol", action="store", type='int', dest="Box_Y_Col", default='1', help="Number of the column (starting in 0) with the Y length of the box")
parser.add_option("-t", "--equil", action="store", type='int', dest="Equil_ps", default='25000', help="Number of picoseconds to consider as equilibration")
parser.add_option("-T", "--temperature", action="store", type='float', dest="Temp", default='310', help="Temperature")
parser.add_option("-i", "--ignore", action="store", type='int', dest="Ignore", default='31', help="Number of lines in the xvg file to ignore")
(options, args)= parser.parse_args()

fname_opt = options.MetricFile
oname_opt = options.OutputFile
x_col = options.Box_X_Col
y_col = options.Box_Y_Col
t_equil = options.Equil_ps
temp = options.Temp
N_ignore = options.Ignore

data = np.genfromtxt(fname_opt, skip_header=N_ignore)
time = data[:,0]
area = np.multiply(data[:,x_col], data[:,y_col])
area_av = np.mean(area[time >= t_equil])
area_std = np.std(area[time >= t_equil])

compress = 10**21*const.k*temp*area_av/(np.mean(np.power(area-area_av,2)))
err1 = 2*np.power(area-area_av,2)*area_std/area_av
err2 = np.mean(err1)
err3 = ((area_std/area_av)**2 + (np.mean(2*np.power(area-area_av,2)*area_std/area_av)/err2)**2)**0.5
compress_std = 10**21*const.k*temp*err3

out = open(oname_opt, "w")
out.write("Isothermal area compressibility modulus (mN/m): \n")
out.write("{:.2f} +/ {:.2f} \nThe deviation was calculated with error propagation rules\n".format(compress, compress_std))
out.close()
