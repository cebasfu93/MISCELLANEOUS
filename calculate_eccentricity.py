import numpy as np
import matplotlib.pyplot as plt
import sys
from optparse import OptionParser

parser=OptionParser()
parser.add_option("-f", "--input", action="store", type='string', dest="Input", default='NP_iner.xvg', help=".xvg file with the moments of inertia along a trajectory")
parser.add_option("-b", "--begin", action="store", type='float', dest="Begin", default='25000', help="Time (ps) to be discarded as equilibration")
parser.add_option("-i", "--ignore", action="store", type='int', dest="Ignore", default='26', help="Number of lines to ignore from the input file")

(options, args)= parser.parse_args()

input_opt = options.Input
begin_opt = options.Begin
ignore_opt = options.Ignore

data = np.genfromtxt(input_opt, skip_header = ignore_opt)
data = data[data[:,0]>=begin_opt,:]
iner = np.mean(data[:,2:], axis=0)
ecc = 1 - np.min(iner)/np.mean(iner)
print("The eccentricity of the system is {:.2f}".format(ecc))
