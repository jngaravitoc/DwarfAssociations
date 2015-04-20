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
        Mag  = data[:,8]
	index = np.where(Mag>-18.81)
        index = index[0]
        return x[index], y[index], z[index], vx[index], vy[index], vz[index], Mag[index]

def stars(x, y, z, vx, vy, vz, Mag):
        index = np.where(Mag<100)
        index = index[0]
        return x[index], y[index], z[index], vx[index], vy[index], vz[index]


def fof(x, y, z, vx, vy, vz, N, snap_fof):
	f = open(snap_fof, "w")
	f.write("%d\n"%N) #points in total 
	f.write("%d\n"%N) #points in 'DM'
	f.write("0\n") #gas
	f.write("0\n") #stars
	f.write("0.01\n") # time
	f.write("0\n") # nactive
	for i in range(len(x)):
    		f.write(("%f \t %f \t %f  \n")%(x[i], y[i], z[i]))
	f.close()
        h = 0.7
        LL_min = 526 # Linking Lenght in Kpc, taken from observational treshold (FOF-observed-associations.ipynb)
        LL_max = 724 # Max Linking Length in Kpc
        os.system(('./../../../HackFOF/src/fof -e %f -m 2  < ' +  snap_fof)%(LL_min*h)) 
        fof_groups = np.loadtxt('fof.grp', skiprows=1)
        N_as_min = len(list(set(fof_groups)))
        ## Esto sobrescribe los datos de las asociaciones--------------------------
        f = open("A_min" + snap_fof, "w") 
	for j in range(len(x)):
		f.write(("%f \t %f \t %f \t %f \t %f \t %f \t %f \n" )%(x[j], y[j], z[j], vx[j], vy[j], vz[j], fof_groups[j]))        
        f.close()
        f = open("A_max" + snap_fof, "w")
        #  [-px <xPeriod>] [-py <yPeriod>] [-pz <zPeriod>] FOF periodic conditions       
        os.system(('./../../../HackFOF/src/fof -e %f -m 2  < '+ snap_fof)%(LL_max*h)) 
	fof_groups = np.loadtxt('fof.grp', skiprows=1)
        N_as_max = len(list(set(fof_groups)))
        for j in range(len(x)):
        	f.write(("%f \t %f \t %f \t %f \t %f \t %f \t %f \n" )%(x[j], y[j], z[j], vx[j], vy[j], vz[j], fof_groups[j]))
        f.close()
	return N_as_min, N_as_max

def dispersiones_x(snap_fof):
        data_min = np.loadtxt("A_min" + snap_fof)
        data_max = np.loadtxt("A_max" + snap_fof)
        x_min = data_min[:,0]
        y_min = data_min[:,1]
        z_min = data_min[:,2]
        vx_min = data_min[:,3]
        vy_min = data_min[:,4]
        vz_min = data_min[:,5]
        N_min = data_min[:,6]
	x_max = data_max[:,0]
        y_max = data_max[:,1]
        z_max = data_max[:,2]
        vx_max = data_max[:,3]
        vy_max = data_max[:,4]
        vz_max = data_max[:,5]
        N_max = data_max[:,6]
       	N_min = len(list(set(fof_groups)))
        sigmax_min = np.zeros(N_min)
        sigmav_min = np.zeros(N_min)
        sigmax_max = np.zeros(N_max)
        sigmav_max = np.zeros(N_max)
	for i in range(1,N_as_min):
        	index = np.where(N_min==i)
                index = index[0]
                x_LLmin = x_min[index]
                y_LLmin = y_min[index]
                z_LLmin = z_min[index]
                vx_LLmin = vx_min[index]
                vy_LLmin = vy_min[index]
                vz_LLmin = vz_min[index]
		Vx_cm = sum(vx_LLmin*M)/sum(M)
    		Vy_cm = sum(vy_LLmin*M)/sum(M)
    		Vz_cm = sum(vz_LLmin*M)/sum(M)
    		X_cm = sum(x_LLmin*M/sum(M))
    		Y_cm = sum(y_LLmin*M/sum(M))
    		Z_cm = sum(z_LLmin*M/sum(M))
    		x_LLmin -=  X_cm 
    		y_LLmin -=  Y_cm 
    		z_LLmin -=  Z_cm 
    		vx_LLmin -= Vx_cm 
    		vy_LLmin -=  Vy_cm 
    		vz_LLmin -= Vz_cm 
    		X = sqrt(x_LLmin**2 + y_LLmin**2 + z_LLmin**2)
    		V = sqrt(vx_LLmin**2 + vy_LLmin**2 + vz_LLmin**2)
    		V_disp = std(V)
    		X_disp = std(X)	        
	for i in range(1,N_as_max):
                index = np.where(N_max==i)
                index = index[0]
                x_LLmax = x_max[index]
                y_LLmax = y_max[index]
                z_LLmax = z_max[index]
                vx_LLmax = vx_max[index]
                vy_LLmax = vy_max[index]
                vz_LLmax = vz_max[index]
                Vx_cm = sum(vx_LLmax*M)/sum(M)
                Vy_cm = sum(vy_LLmax*M)/sum(M)
                Vz_cm = sum(vz_LLmax*M)/sum(M)
                X_cm = sum(x_LLmax*M/sum(M))
                Y_cm = sum(y_LLmax*M/sum(M))
                Z_cm = sum(z_LLmax*M/sum(M))
                x_LLmax -=  X_cm                     
                y_LLmax -=  Y_cm                  
                z_LLmax -=  Z_cm                  
                vx_LLmax -= Vx_cm                
                vy_LLmax -=  Vy_cm               
                vz_LLmax -= Vz_cm                 
                X = sqrt(x_LLmax**2 + y_LLmax**2 + z_LLmax**2)
                V = sqrt(vx_LLmax**2 + vy_LLmax**2 + vz_LLmax**2)
                V_disp = std(V)
                X_disp = std(X)  

#def 3dplot(x, y, z)
			
	

