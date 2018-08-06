import numpy as np
from optparse import OptionParser
import os
import sys
import re
import math as m
import random as random

def rotateXYZ(psi, theta, phi):
    c1 = m.cos(psi)
    c2 = m.cos(theta)
    c3 = m.cos(phi)
    s1 = m.sin(psi)
    s2 = m.sin(theta)
    s3 = m.sin(phi)
    rot_mat = [[c1*c2,  c1*s2*s3-c3*s1,     s1*s3+c1*c3*s2],\
    [c2*s1,     c1*c3+s1*s2*s3,     c3*s1*s2-c1*s3],\
    [-s2,       c2*s3,      c2*c3]]
    return rot_mat

def rotate_body(x, y, z, rep):
    random.seed(rep)
    a1, a2, a3 = random.random()*2*m.pi-m.pi, random.random()*2*m.pi-m.pi, random.random()*2*m.pi-m.pi
    body = np.column_stack((x,y,z))
    rotated_body = np.zeros(np.shape(body))
    rotation = rotateXYZ(a1, a2, a3)
    for i in range(len(x)):
        rotated_body[i] = np.dot(rotation, body[i])
    return rotated_body[:,0], rotated_body[:,1], rotated_body[:,2]

parser=OptionParser()
parser.add_option("-n", "--np", action="store", type='string', dest="NanoParticle", default='NP.gro', help="Name of the NP's gro file.")
parser.add_option("-x", "--metal", action="store", type='string', dest="Metal", default='AU', help="Atom name of the metallic core.")
parser.add_option("-m", "--mem", action="store", type="string", dest="Membrane", default="MEM.gro", help="Name of the membrane's gro file")
parser.add_option("-d", "--dist", action="store", type="float", dest="Distance", default="4.0", help="Distance between the center of coordinates of the NP and the bilayer's midplane")
parser.add_option("-o", "--output", action="store", type="string", dest="OutName", default="NP-MEM.gro", help="Name of the output gro file")
parser.add_option("-e", "--embed", action="store", type="float", dest="Embed", default="0", help="Defines whether if the NP will be embeded in the membrane or not")
parser.add_option("-z", "--sizebox", action="store", type="float", dest="Zeta", default="5.0", help="Minimum distance between the solute and the box (in Z)")
parser.add_option("-r", "--replica", action="store", type="int", dest="Replica", default="0", help="Number of replica (RSEED). If set to 0, the initial conformation is taken.")
(options, args)= parser.parse_args()
np_opt=options.NanoParticle
metal_opt=options.Metal
mem_opt=options.Membrane
out_opt=options.OutName
dist_opt=options.Distance
embed_opt=bool(options.Embed)
zeta_opt=options.Zeta
replica_opt = options.Replica

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
    #x_np=np.append(x_np, float(nano[i][-24:-16]))
    #y_np=np.append(y_np, float(nano[i][-16:-8]))
    #z_np=np.append(z_np, float(nano[i][-8:]))
    x_np=np.append(x_np, float(nano[i][-48:-41]))
    y_np=np.append(y_np, float(nano[i][-40:-33]))
    z_np=np.append(z_np, float(nano[i][-32:-25]))
    if metal_opt in nano[i]:
        au[i-2]=True

if replica_opt != 0:
    x_np, y_np, z_np = rotate_body(x_np, y_np, z_np, replica_opt)

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
    #out_file.write(nano[i][:-29].rjust(15))
    out_file.write(nano[i][:-53].rjust(15))

    out_file.write(str(at).rjust(5))
    out_file.write("{:.3f}".format(x_np[i-2]).rjust(8)+ "{:.3f}".format(y_np[i-2]).rjust(8)+ "{:.3f}".format(z_np[i-2]).rjust(8))

    #out_file.write("\n")
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
