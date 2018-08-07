import numpy as np
import scipy as sci
from optparse import OptionParser

parser=OptionParser()
parser.add_option("-f", "--input", action="store", type='string', dest="Input", default='RDF.xvg', help=".xvg file with the RDF's")
parser.add_option("-i", "--ignore", action="store", type='int', dest="Ignore", default='25', help="Number of lines to ignore in the .xvg file")

(options, args)= parser.parse_args()

input_opt=options.Input
ignore_opt=options.Ignore

data = np.genfromtxt(input_opt, dtype='float', skip_header=ignore_opt)
means = np.zeros(len(data[0,:])-1)

print(type(means))

def integrate(rdf, a, b):
    N = len(rdf) - 1
    norm = (b-a)/N*(rdf[0]+rdf[-1])*0.5
    for i in range(1, N-1):
        norm += (b-a)/N*rdf[i]
    return norm

def normalize_rdf(rdf, a, b):
    rdf = rdf/integrate(rdf, a, b)
    return rdf

def get_mean(rdf, r, a, b):
    N = len(rdf) - 1
    val = (b-a)/N*(rdf[0]*r[0]+rdf[-1]*r[-1])*0.5
    for i in range(1, N-1):
        val += (b-a)/N*rdf[i]*r[i]
    return val

for i in range(1, len(data[0,:])):
    data[:,i] = normalize_rdf(data[:,i], data[0,0], data[-1,0])
    means[i-1] = get_mean(data[:,i], data[:,0], data[0,0], data[-1,0])
    print("RDF number {:.0f} has a mean of {:.3f} nm".format(i, means[i-1]))
