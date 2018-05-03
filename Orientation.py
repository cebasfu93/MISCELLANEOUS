import numpy as np
from optparse import OptionParser
import os
import sys
import re

parser=OptionParser()
parser.add_option("-n", "--np", action="store", type='string', dest="NanoParticle", default='NP.gro', help="Name of the NP's gro file.")
parser.add_option("-x", "--metal", action="store", type='string', dest="Metal", default='AU', help="Atom name of the metallic core.")
parser.add_option("-m", "--mem", action="store", type="string", dest="Membrane", default="MEM.gro", help="Name of the membrane's gro file")
parser.add_option("-d", "--dist", action="store", type="float", dest="Distance", default="4.0", help="Distance between the center of coordinates of the NP and the bilayer's midplane")
parser.add_option("-o", "--output", action="store", type="string", dest="OutName", default="NP-MEM.gro", help="Name of the output gro file")
parser.add_option("-e", "--embed", action="store", type="float", dest="Embed", default="0", help="Defines whether if the NP will be embeded in the membrane or not")
parser.add_option("-z", "--sizebox", action="store", type="float", dest="Zeta", default="5.0", help="Minimum distance between the solute and the box (in Z)")
(options, args)= parser.parse_args()
np_opt=options.NanoParticle
metal_opt=options.Metal
mem_opt=options.Membrane
out_opt=options.OutName
dist_opt=options.Distance
embed_opt=bool(options.Embed)
zeta_opt=options.Zeta

nano=np.genfromtxt(np_opt, dtype="str", delimiter="\n")
mem=np.genfromtxt(mem_opt, dtype="str", delimiter="\n")

N_np=len(nano)
N_mem=len(mem)
N_tot=N_np+N_mem-6

out_file=open(out_opt, "w")

out_file.write(np_opt + "-" + mem_opt + "\n")
out_file.write(str(N_tot) + "\n")

x_np=np.array([])
y_np=np.array([])
z_np=np.array([])
au=np.zeros(N_np-3, dtype=bool)
for i in range(2, N_np-1):
    x_np=np.append(x_np, float(nano[i][-48:-41]))
    y_np=np.append(y_np, float(nano[i][-40:-33]))
    z_np=np.append(z_np, float(nano[i][-32:-25]))
    if metal_opt in nano[i]:
        au[i-2]=True

x_com_np=np.average(x_np[au])
y_com_np=np.average(y_np[au])
z_com_np=np.average(z_np[au])

x_mem=np.array([])
y_mem=np.array([])
z_mem=np.array([])
for i in range(2, N_mem-1):
    x_mem=np.append(x_mem, float(mem[i][-48:-41]))
    y_mem=np.append(y_mem, float(mem[i][-40:-33]))
    z_mem=np.append(z_mem, float(mem[i][-32:-25]))
x_com_mem=np.average(x_mem)
y_com_mem=np.average(y_mem)
z_com_mem=np.average(z_mem)

x_np=x_np-x_com_np
y_np=y_np-y_com_np
z_np=z_np-z_com_np

x_mem=x_mem-x_com_mem
y_mem=y_mem-y_com_mem
z_mem=z_mem-z_com_mem

if not embed_opt:
    z_np=z_np+dist_opt

x_com, y_com, z_com = np.average(np.append(x_np, x_mem)), np.average(np.append(y_np, y_mem)), np.average(np.append(z_np, z_mem))

x_np=x_np-x_com
y_np=y_np-y_com
z_np=z_np-z_com
x_mem=x_mem-x_com
y_mem=y_mem-y_com
z_mem=z_mem-z_com

z_com_np=np.average(z_np[au])
z_com_mem=np.average(z_mem)

at=0
for i in range(2, N_np-1):
    at+=1
    out_file.write(nano[i][:-53].rjust(15))
    out_file.write(str(at).rjust(5))
    out_file.write("{:.3f}".format(x_np[i-2]).rjust(8)+ "{:.3f}".format(y_np[i-2]).rjust(8)+ "{:.3f}".format(z_np[i-2]).rjust(8))
    out_file.write(nano[i][-24:] + "\n")


for i in range(2, N_mem-1):
    at+=1
    out_file.write(mem[i][:-53].rjust(15))
    out_file.write(str(at%100000).rjust(5))
    out_file.write("{:.3f}".format(x_mem[i-2]).rjust(8) + "{:.3f}".format(y_mem[i-2]).rjust(8) + "{:.3f}".format(z_mem[i-2]).rjust(8))
    out_file.write(mem[i][-24:]+"\n")

x_box, y_box, z_box= float(mem[-1].split()[0]), float(mem[-1].split()[1]), float(mem[-1].split()[2])
all_z=np.append(z_np, z_mem)
if not embed_opt:
    z_box=z_com_np - z_com_mem + dist_opt + zeta_opt
out_file.write("{:.5f} {:.5f} {:.5f}".format(x_box, y_box, z_box) + "\n")
out_file.close()
