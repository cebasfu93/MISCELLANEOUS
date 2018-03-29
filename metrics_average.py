import numpy as np
from optparse import OptionParser
import os
import sys
import re

parser=OptionParser()
parser.add_option("-f", "--input", action="store", type='string', dest="MetricFile", default='NP-MEM_pullx.xvg', help=".xvg file with the time and properties.")
parser.add_option("-p", "--property", action="store", type='string', dest="Property", default='inertia', help="Property to extract. Admissible values: inertia, gyration, sasa, rmsd")
parser.add_option("-t", "--time", action="store", type='int', dest="EqTime", default='25000', help="Time to be considered as equilibration (discarded from metrics).")
(options, args)= parser.parse_args()

fname_opt = options.MetricFile
prop_opt = options.Property
time_opt = options.EqTime

def get_PROP(DATA, col):
    prop_av = np.average(DATA[DATA[:,0] >= time_opt, col])
    prop_std = np.std(DATA[DATA[:,0] >= time_opt, col])
    return prop_av, prop_std

if prop_opt == 'inertia':
    data = np.genfromtxt(fname_opt, skip_header=26)
    inert_av, inert_std = get_PROP(data, 1)
    print(r"Total moment of inertia (amu nm^2): {:.3f} +/- {:.3f}".format(inert_av, inert_std))
    iner1_av, iner1_std = get_PROP(data, 2)
    print(r"First moment of inertia (amu nm^2): {:.3f} +/- {:.3f}".format(iner1_av, iner1_std))
    iner2_av, iner2_std = get_PROP(data, 3)
    print(r"Second moment of inertia (amu nm^2): {:.3f} +/- {:.3f}".format(iner2_av, iner2_std))
    iner3_av, iner3_std = get_PROP(data, 4)
    print(r"Third moment of inertia (amu nm^2): {:.3f} +/- {:.3f}".format(iner3_av, iner3_std))
    iner_mom = [iner1_av,  iner2_av, iner3_av]
    ecc = 1 - np.min(iner_mom)/np.average(iner_mom)
    print("Eccentricity: {:.3f}".format(ecc))

elif prop_opt == 'gyration':
    data = np.genfromtxt(fname_opt, skip_header=26)
    gyrt_av, gyrt_std = get_PROP(data, 1)
    print(r"Radius of gyration (nm): {:.3f} +/- {:.3f}".format(gyrt_av, gyrt_std))
    gyr1_av, gyr1_std = get_PROP(data, 2)
    print(r"Radius of gyration in X (nm): {:.3f} +/- {:.3f}".format(gyr1_av, gyr1_std))
    gyr2_av, gyr2_std = get_PROP(data, 3)
    print(r"Radius of gyration in Y (nm): {:.3f} +/- {:.3f}".format(gyr2_av, gyr2_std))
    gyr3_av, gyr3_std = get_PROP(data, 4)
    print(r"Radius of gyration in Z (nm): {:.3f} +/- {:.3f}".format(gyr3_av, gyr3_std))

elif prop_opt == 'sasa':
    data = np.genfromtxt(fname_opt, skip_header=23)
    sasa_av, sasa_std = get_PROP(data, 1)
    print(r"SASA (nm^2): {:.3f} +/- {:.3f}".format(sasa_av, sasa_std))

elif prop_opt == 'rmsd':
    data = np.genfromtxt(fname_opt, skip_header=17)
    rmsd_av, rmsd_std = get_PROP(data, 1)
    print(r"RMSD (nm): {:.3f} +/- {:.3f}".format(rmsd_av, rmsd_std))

else:
    print("Invalid value in Property (-p)")
