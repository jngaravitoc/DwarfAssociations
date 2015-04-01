import numpy as np
import matplotlib.pyplot as plt

AHF_associations = np.loadtxt("/home/jngaravito57/Documents/codes/ahf-v1.0-084/bin/All.snap.z0.000.AHF_particles", skiprows=1)

data = np.loadtxt("/home/jngaravito57/Documents/github/DwarfAssociations/data/B64_WM5_10909_LG_7Mpc_2048/halos.ascii")

x = data[:,0]
y = data[:,1]
z = data[:,2]
vx = data[:,3]
vy = data[:,4]
vz = data[:,5]
m = data[:,6]

ID_halo = np.int_(AHF_associations[:,0])
Association = AHF_associations[:,1]

N_halo = int(max(Association)+1)


print "El numero de asociaciones es: \n", N_halo
print min(Association), max(Association)

def rv_disp(x, y, z, vx, vy, vz, m):
        X_cm = sum(x*m)/sum(m)
        Y_cm = sum(y*m)/sum(m)
        Z_cm = sum(z*m)/sum(m)
        Vx_cm = sum(vx*m)/sum(m)
        Vy_cm = sum(vy*m)/sum(m)
        Vz_cm = sum(vz*m)/sum(m)
        x = x - X_cm
        y = y - Y_cm
        z = z - Z_cm
        vx = vx - Vx_cm
        vy = vy - Vy_cm
        vz = vz - Vz_cm
        R = np.sqrt(x**2 + y**2 + z**2)
        V = np.sqrt(vx**2 + vy**2 + vz**2)
        sigmar = np.std(R)
        sigmav = np.std(V)
        return sigmar, sigmav


for i in range(N_halo):
	index = np.where(Association==i)
        index = index[0]
        sigmar, sigmav = rv_disp(x[ID_halo[index]], y[ID_halo[index]], z[ID_halo[index]], vx[ID_halo[index]], vy[ID_halo[index]], vz[ID_halo[index]], m[ID_halo[index]])    
        print len(ID_halo[index]) 
	#print sigmar, sigmav

