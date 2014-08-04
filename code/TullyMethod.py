import numpy as np 

filename = "../data/B64_WM5_10909_LG_7Mpc_2048/CLUES-basic-data.txt"
filename2  = "100distances.txt"

def reading_data(filename):

   data = np.loadtxt(filename)

   X = data[:, 2]
   Y = data[:, 3]
   Z = data[:, 4]
   M = data[:, 8]

   return X, Y, Z, M


def distance(filename):
   X, Y, Z, M = reading_data(filename)
   d = []
   for i in range(len(X)):
	dist = np.sqrt(X[i]**2 + Y[i]**2 + Z[i]**2) 
        d.append(dist)
   f = open("distances.txt", "w")
   f.write("#Distances    VirialMass" + "\n")
   for i in range(len(X)):
        f.write(str(d[i]) + "  " + str(M[i]) + "\n")
   f.close()

def CM(filename2):
   data = np.loadtxt(filename2)
   r = data[:,0]
   M = data[:,1]
   r_cm2 = []
   for i in range(len(M)):
	for j in range(len(M)):
                if i != j:
			r_cm = M[i]*r[i]**2/(M[j] + M[i]) + (M[j]*r[j]**2/(M[i] + M[j])) - (M[i]*M[j]*(r[i]-r[j])**2/(M[i]+M[j])**2) 
			r_cm2.append(r_cm)
   for i in range(len(r_cm2)):
   	print r_cm2[i]
#distance(filename)

def merging(cm_R):
   index = np.where(cm_R==min(cm_R))
   

CM(filename2)
