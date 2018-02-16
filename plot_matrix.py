import numpy as np
from optparse import OptionParser
import matplotlib.pyplot as plt
import os
import sys

parser=OptionParser()
parser.add_option("-f", "--gro", action="store", type='string', dest="InputFile", default='data.dat', help="Name of the file with the data")
parser.add_option("-o", "--out", action="store", type='string', dest="OutputFile", default='matrix.pdf', help="Name of the output image")
(options, args)= parser.parse_args()
inname_opt=options.InputFile
outname_opt=options.OutputFile

def plot_matrix(matrix_func):
    matrix=np.genfromtxt(matrix_func)
    ave=round(np.average(matrix),3)
    fig=plt.figure()
    plt.imshow(matrix)
    plt.xlabel("Average: "+str(ave))
    plt.colorbar()
    plt.title(matrix_func)
    plt.savefig(outname_opt)
    plt.close()
plot_matrix(inname_opt)
