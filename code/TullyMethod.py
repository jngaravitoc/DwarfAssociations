import numpy as np
from array import array 

filename = "../data/B64_WM5_10909_LG_7Mpc_2048/data.txt"
filename2  = "distances.txt"

def reading_data(filename):

   data = np.loadtxt(filename)

   X = data[:, 2]
   Y = data[:, 3]
   Z = data[:, 4]
   M = data[:, 8]

   X = X[0:100]
   Y = Y[0:100]
   Z = Z[0:100]

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
        f.write(str(d[i]) + "  " + str(M[i]) + "  " + str(X[i]) + "   " + str(Y[i]) + "   " + str(Z[i]) + "\n")
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
                        print "changos"
   #for i in range(len(r_cm2)):
   return r_cm2
#distance(filename)

def merging(filename2):
   cm_R = CM("distances.txt")
   print "hola"
   data = np.loadtxt("distances.txt")
   X = data[:,0]
   Y = data[:,1]
   longitud =  len(data)-1 # por el encabezado
   index = np.where(cm_R==min(cm_R))
   minimo =  np.amin(index)
   halo_j = int(minimo/longitud) # Hallando el indice de la particula 2.
   halo_i = minimo - (halo_j*longitud) # Hallando el indice de la particula 1. 
   print np.sqrt(cm_R[minimo]),"posicion particula 1", halo_i, "posicion particula 2", halo_j
   print len(X)
   x = np.delete(X,[halo_i, halo_j])
   y = np.delete(Y,[halo_i, halo_j])
   XX = np.append(x, np.sqrt(min(cm_R))) 
   YY = np.append(y, Y[halo_i]+Y[halo_j])
   f = open("distances.txt", "w")
   for i in range(len(XX)):
   	f.write(str(XX[i]) + "  " + str(YY[i]) + "\n")
   f.close()
   merging_rate = len(XX)
   return merging_rate

distance(filename)
x = merging("distances.txt")
#for i in range(2):
while x>4:
	x = merging("distances.txt")
#print merging_rate



