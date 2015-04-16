import numpy as np
import scipy as sp
import os


def loading_snapshot(snap_name):
	data = np.loadtxt(snap_name)
        x = data[:,1]
        y = data[:,2]
        z = data[:,3]
        vx = data[:,4]
        vy = data[:,5]
        vz = data[:,6]
        Mag  = data[:,7]
	index = where(Mag>8.81)
        index = index[0]
        return x[index], y[index], z[index], vx[index], vy[index], vz[index], Mag[index]

def stars(x, y, z, vx, vy, vz, Mag):
        index = where(Mag<100)
        index = index[0]
        return x[index], y[index], z[index], vx[index], vy[index], vz[index]


def fof(x, y, z, vx, vy, vz, N, snap_fof):
	f = open(snap_fof, "w")
	f.write("%d\n"%N) #points in total 
	f.write("%d\n"%N) #points in 'DM'
	f.write("0\n") #gas
	f.write("%d\n"%) #stars
	f.write("0.01\n") # time
	f.write("0\n") # nactive
	for i in range(len(x)):
    		f.write(("%f \t %f \t %f  \n")%(x[i], y[i], z[i]))
	f.close()
        h = 0.7
        LL_min = 526 # Linking Lenght in Kpc, taken from observational treshold (FOF-observed-associations.ipynb)
        LL_max = 724 # Max Linking Length in Kpc
        os.system(('./../../../HackFOF/src/fof -e %f -m 2 < ' snap_fof)%(LL_min/h)) 
        fof_groups = loadtxt('fof.grp', skiprows=1)
        N_as = len(list(set(fof_groups)))
	for i in range(1,N_as):
    		index = where(fof_groups==i)
    		index = index[0]
    		x_LLmin = x[index]
    		y_LLmin = y[index]
    		z_LLmin = z[index]
        
        os.system(('./../../../HackFOF/src/fof -e %f -m 2 < ' snap_fof)%(LL_max/h)) 
	fof_groups = loadtxt('fof.grp', skiprows=1)
        N_as = len(list(set(fof_groups)))
        for i in range(1,N_as):
                index = where(fof_groups==i)
                index = index[0]
                x_LLmax = x[index]
                y_LLmax = y[index]
                z_LLmax = z[index]


