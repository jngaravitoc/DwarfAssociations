import numpy as np
import scipy as sp

data = np.loadtxt("../data/B64_WM5_10909_LG_7Mpc_2048/data.txt")

x = data[0:10,2]
y = data[0:10,3]
z = data[0:10,4]
m = data[0:10,8]

l = len(x)

for i in range(2):
    f = open("../data/Distances/distances"+str(i)+".txt", 'a')
    f.write("Halo ID"+ "   " + "Distance(kpc)" + "  " + "Potencial" + "\n")
    d = []
    for j in range(l):
        if i!=j:
            dist = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2 + (z[i]-z[j])**2)
            phi = m[i]*m[j]/dist
            #d.append(dist)
            f.write(str(j)+ "  "+ str(dist)+ "  " + str(phi) + "\n")
f.close()
