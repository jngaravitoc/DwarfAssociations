import numpy as np 

data = np.loadtxt("rmax.dat")

x = data[:,0]
y = data[:,1]
z = data[:,2]
r = data[:,3]/100.0


Nhalo = 5
distancia = np.sqrt((x[Nhalo]-x[Nhalo:])**2 + (y[Nhalo]-y[Nhalo:])**2 + (z[Nhalo]-z[Nhalo:])**2)

index = np.where(distancia >  r[Nhalo])

print "Numero de halos fuera del R:vir ", len(x[index]), "Numero de Halos: ", len(x)
print "radio virial M[1]",r[Nhalo]
#for i in range(len(distancia)):
#	print distancia[i]
 
