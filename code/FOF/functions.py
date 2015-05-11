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
	print "This is N:", N
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
	print "Number of Associations min L min LL", N_as_min
        f1 = open("data/A_min" + snap_fof, "w") 
	for j in range(len(x)):
		f1.write(("%f \t %f \t %f \t %f \t %f \t %f \t %f \n" )%(x[j], y[j], z[j], vx[j], vy[j], vz[j], fof_groups[j]))        
        f1.close()
        #  [-px <xPeriod>] [-py <yPeriod>] [-pz <zPeriod>] FOF periodic conditions       
        os.system(('./../../../HackFOF/src/fof -e %f -m 2  -px 75000 -py 75000 -pz 75000 < '+ snap_fof)%(LL_max*h)) 
	fof_groups = np.loadtxt('fof.grp', skiprows=1)
	groups2 = list(fof_groups)
        N_as_max = len(list(set(fof_groups)))
	print "Numer of Associations max LL", N_as_max
        f2 = open("data/A_max" + snap_fof, "w")
	for j in range(len(x)):
        	f2.write(("%f \t %f \t %f \t %f \t %f \t %f \t %f \n" )%(x[j], y[j], z[j], vx[j], vy[j], vz[j], fof_groups[j]))
        f2.close()
	


###########################################################
#                                                         #
#  N_associations find the number of members per assoc    #
#  it also returns the maximum number of members in an    #
#  association                                            #
###########################################################

def N_associations(snap_fof):
	N_count_min = []
	N_count_max = []
        Asso_min = []
	Asso_max = []
	data_min = np.loadtxt("data/A_min" + snap_fof)
	data_max = np.loadtxt("data/A_max" + snap_fof)
        Nasso_min = data_min[:,6]
	Nasso_max = data_max[:,6] 
        L_min = list(Nasso_min)
	L_max = list(Nasso_max)
        N_min = len(list(set(Nasso_min)))
 	N_max = len(list(set(Nasso_max)))
        for i in range(N_min):
		x_min = L_min.count(i)
                #if x<25:
		N_count_min.append(x_min)
                Asso_min.append(i)
	for j in range(N_max):
		x_max = L_max.count(j)
		N_count_max.append(x_max)
		Asso_max.append(j)
	X_min = np.sort(N_count_min)
	X_max = np.sort(N_count_max) 
	return N_count_min, Asso_min, X_min[-1], N_count_max, Asso_max, X_max[-1]

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
        N_as_min = len(list(set(N_min)))
        N_as_max = len(list(set(N_max)))
        sigmax_min = []
        sigmax_max = []
	sigmav_min = []
        sigmav_max = []
        a, b, Mem_min, c, d, Mem_max = N_associations(snap_fof)
	for i in range(int(min(list(set(N_min)))),int(max(list(set(N_min)))+1)):
        	index = np.where(N_min==i)
                index = index[0]
		#print "index=", len(index)
                if (len(index)<Mem_min):
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
        	if (len(index)<Mem_max):
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

	
def threedplot(snap_fof, N):	
	data_min = np.loadtxt("data/A_min" + snap_fof)
        #data_max = np.loadtxt("data/A_max" + snap_fof)
	x_min = data_min[:,0]
        y_min = data_min[:,1]
        z_min = data_min[:,2]
        N_min = data_min[:,6]
	#N_as_min = len(list(set(N_min)))
        #N_as_max = len(list(set(N_max)))
        index = np.where(N_min==N)
        index = index[0]
        X = x_min[index]
        Y = y_min[index]
        Z = z_min[index]
	return X, Y, Z

##################################################
#                                                #
#                     DARKS                      #  
#                                                #
##################################################


def scatter_plot(snap_fof):
	data_min = np.loadtxt("data/A_min" + snap_fof)
	x_min = data_min[:,0]
	y_min = data_min[:,1]
	z_min = data_min[:,2]
	plt.scater(x, y, z)

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
	noassdm = 0
	for i in range(Nass):
		index = np.where(NasssDM == i)
		index = index[0]
		if len(index) > 25:
			noassdm == i
	index2 = np.where(ass != noassdm)
	XDM = x_dm[index2]
	YDM = y_dm[index2]
	ZDM = z_dm[index2]

	index3 = np.where((XDM == XS) & (YDM == YS) & (ZDM == ZS) )
	index3 = index3[0]
	index4 = linspace(0, len(XDM), len(XDM))
			
	#index = np.where((x_dm == x_s)&&(y_dm == y_s)&&(z_dm==z_s))
	

