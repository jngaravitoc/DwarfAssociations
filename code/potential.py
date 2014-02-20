import numpy as np

data = np.loadtxt("../data/B64_WM5_10909_LG_7Mpc_2048/data.txt")

x = data[:,2]
y = data[:,3]
z = data[:,4]
m = data[:,8]

l = len(x)

xmin = min(x)
xmax = max(x)

ymin = min(y)
ymax = max(y)

zmin = min(z)
zmax = max(z)

f = open("../data/Distances/distances.txt", 'w')
f.write("X(pc)"+ "   " + "Y(pc)" + "  " + "Z(pc)" + "  " + "Potencial" + "\n")
    
for i in range(l):
    u = []
    for j in range(l):
        if i!=j:
            dist = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2 + (z[i]-z[j])**2)
            phi = m[i]*m[j]/dist
            u.append(phi)
            #d.append(dist)
    U = sum(u)
    f.write(str(x[i])+ "  "+ str(y[i])+ "  " + str(z[i]) + "  " + str(U) + "\n")
f.close()

