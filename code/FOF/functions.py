import numpy as np
import scipy as sp
import os

# loading snaphot: Read the data from the snapshots.

def loading_snapshot(snap_name):
	data = np.loadtxt(snap_name)
        x = data[:,1]
        y = data[:,2]
        z = data[:,3]
        vx = data[:,4]
        vy = data[:,5]
        vz = data[:,6]
        Mag  = data[:,8]
        return x, y, z, vx, vy, vz, Mag

# stars select the baryons from the snapshot, and select those who are visible to the current instruments (Mag<-8)

def stars(x, y, z, vx, vy, vz, Mag):
        index = np.where(Mag<-8)# Acording to Tully. et al 2006 this is the faintest observed galaxy
        index = index[0]
        return x[index], y[index], z[index], vx[index], vy[index], vz[index]



# fof runs the fof algorithm.

def fof(x, y, z, vx, vy, vz, N, snap_fof):
	f = open(snap_fof, "w")
	f.write("%d\n"%N) #points in total 
	f.write("%d\n"%N) #points in 'DM'
	f.write("0\n") #gas
	f.write("0\n") #stars
	f.write("0.01\n") # time
	f.write("0\n") # nactive
        # up to here is the fof header format
	for i in range(len(x)):
    		f.write(("%f \t %f \t %f  \n")%(x[i], y[i], z[i]))
	f.close()
        h = 0.7
        # here I define the linking lenghts 
        LL_min = 526 # Linking Lenght in Kpc, taken from observational treshold (FOF-observed-associations.ipynb)
        LL_max = 724 # Max Linking Length in Kpc
        os.system(('./../../../HackFOF/src/fof -e %f -m 2  -px 75000 -py 75000 -pz 75000 < ' +  snap_fof)%(LL_min*h)) 
        fof_groups = np.loadtxt('fof.grp', skiprows=1)
	groups1 = list(fof_groups)
	N_as_min = len(list(set(fof_groups)))
	new_fof_min = 0
	for k in range(N_as_min):
		XX = groups1.count(k)
		if XX < 30:
			new_fof_min += 1	
        ## Esto sobrescribe los datos de las asociaciones--------------------------
        f = open("data/A_min" + snap_fof, "w") 
	for j in range(len(x)):
		f.write(("%f \t %f \t %f \t %f \t %f \t %f \t %f \n" )%(x[j], y[j], z[j], vx[j], vy[j], vz[j], fof_groups[j]))        
        f.close()
        f = open("data/A_max" + snap_fof, "w")
        #  [-px <xPeriod>] [-py <yPeriod>] [-pz <zPeriod>] FOF periodic conditions       
        os.system(('./../../../HackFOF/src/fof -e %f -m 2  -px 75000 -py 75000 -pz 75000 < '+ snap_fof)%(LL_max*h)) 
	fof_groups = np.loadtxt('fof.grp', skiprows=1)
	groups2 = list(fof_groups)
        N_as_max = len(list(set(fof_groups)))
	new_fof_max = 0
        for k in range(N_as_min):
      		XX = groups2.count(k)
                if XX < 30:
                        new_fof_max += 1
        for j in range(len(x)):
        	f.write(("%f \t %f \t %f \t %f \t %f \t %f \t %f \n" )%(x[j], y[j], z[j], vx[j], vy[j], vz[j], fof_groups[j]))
        f.close()
	return new_fof_min, new_fof_max


###########################################################
#                                                         #
#  N_associations find the number of members per group    #
#                                                         #
###########################################################

def N_associations(name):
	N_count = []
        Asso = []
	data = np.loadtxt("data/" + name)
        Nasso = data[:,6]
        L = list(Nasso)
        N = len(list(set(Nasso)))
        for i in range(N):
		x = L.count(i)
                if x<25:
			N_count.append(x)
                	Asso.append(i)
	return N_count, Asso

##########################################################
#                                                        #
# Disperiosnes: Finds the dispersions of  every group    #
#                                                        #
##########################################################

def dispersiones(snap_fof):
        data_min = np.loadtxt("data/A_min" + snap_fof)
        data_max = np.loadtxt("data/A_max" + snap_fof)
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
       	N_min = data_min[:,6]
        N_as_min = len(list(set(N_min)))
        N_as_max = len(list(set(N_max)))
        sigmax_min = []
        sigmav_min = []
        sigmax_max = []# The +1 is beacuse the snap17 max have all the memebers in 1 a in 2 so it doesnt have 0 and sigmav_max brokes
        sigmav_max = []
        #rint "N ass = ", N_as_min
	for i in range(int(min(list(set(N_min)))),int(max(list(set(N_min)))+1)):
        	index = np.where(N_min==i)
                index = index[0]
		#print "index=", len(index)
                if (len(index)<25):
			x_LLmin = x_min[index]
                	y_LLmin = y_min[index]
                        z_LLmin = z_min[index]
                	#print "test---------",i
			vx_LLmin = vx_min[index]
			vy_LLmin = vy_min[index]
                	vz_LLmin = vz_min[index]
			M = 1.0
			Vx_cm = sum(vx_LLmin*M)/len(x_LLmin)
    			Vy_cm = sum(vy_LLmin*M)/len(x_LLmin)
    			Vz_cm = sum(vz_LLmin*M)/len(x_LLmin)
    			X_cm = sum(x_LLmin*M)/len(x_LLmin)
    			Y_cm = sum(y_LLmin*M)/len(x_LLmin)
    			Z_cm = sum(z_LLmin*M)/len(x_LLmin)
    			x_LLmin -= X_cm 
    			y_LLmin -= Y_cm 
    			z_LLmin -= Z_cm 
    			vx_LLmin -= Vx_cm 
    			vy_LLmin -= Vy_cm 
    			vz_LLmin -= Vz_cm 
    			X = np.sqrt(x_LLmin**2 + y_LLmin**2 + z_LLmin**2)
    			V = np.sqrt(vx_LLmin**2 + vy_LLmin**2 + vz_LLmin**2)
    			sigmav_min.append(np.std(V))
    			sigmax_min.append(np.std(X))	       
	for i in range(int(min(list(set(N_max)))),int(max(list(set(N_max)))+1)):
		#print "Nass max = ", N_as_max
                index = np.where(N_max==i)
                index = index[0]
        	if (len(index)<25):
	        	x_LLmax = x_max[index]
                	y_LLmax = y_max[index]
                	z_LLmax = z_max[index]
	        	vx_LLmax = vx_max[index]
                	vy_LLmax = vy_max[index]
                	vz_LLmax = vz_max[index]
                	M = 1.0
			#print len(x_LLmax)
                	Vx_cm = sum(vx_LLmax*M)/float(len(x_LLmax))
                	Vy_cm = sum(vy_LLmax*M)/float(len(x_LLmax))
                	Vz_cm = sum(vz_LLmax*M)/float(len(x_LLmax))
                	X_cm = sum(x_LLmax*M)/float(len(x_LLmax))
                	Y_cm = sum(y_LLmax*M)/float(len(x_LLmax))
                	Z_cm = sum(z_LLmax*M)/float(len(x_LLmax))
                	x_LLmax -=  X_cm                     
                	y_LLmax -=  Y_cm                  
                	z_LLmax -=  Z_cm                  
                	vx_LLmax -= Vx_cm                
                	vy_LLmax -=  Vy_cm               
                	vz_LLmax -= Vz_cm                 
                	X = np.sqrt(x_LLmax**2 + y_LLmax**2 + z_LLmax**2)
                	V = np.sqrt(vx_LLmax**2 + vy_LLmax**2 + vz_LLmax**2)
	          	sigmav_max.append(np.std(V))
                	sigmax_max.append(np.std(X)) 
	#print "-----DONE------" 
	return sigmax_min, sigmav_min, sigmax_max, sigmav_max
#def 3dplot(x, y, z)
			
	

##################################################
#                                                #
#                     DARKS                      #  
#                                                #
##################################################

def darks():
	DM = np.loadtxt("data/A_minFOFDMIllustris_group_26.dat")
	stars = np.loadtxt("data/A_minFOF_starsIllustris_group_26.dat")
	x_dm = DM[:,0]
        y_dm = DM[:,1]
        z_dm = DM[:,2]
	x_s = stars[:,0]
        y_s = stars[:,1]
        z_s = stars[:,2]
	assdm = DM[:,6]
	asss = stars[:,6]
	Nasss = set(list(asss))
	NassDM = set(list(assdm))
	noass =  0 
	for i in range(Nasss):
		if list(asss).count > 25:
			noass = i
	index1 = np.where(asss != noass)
	XS = x_s[index1]
	YS = y_s[index1]
	ZS = z_z[index1]	
	print Nasss, NassDM
	for i in range(Nass):
		index = np.where(NasssDM == i)
		index = index[0]
		if len(index) < 25:
			index2 = np.where(assdm == i)
			XDM = x_dm[index2]
			YDM = y_dm[index2]
			ZDM = z_dm[index2]
			
	#index = np.where((x_dm == x_s)&&(y_dm == y_s)&&(z_dm==z_s))
	

