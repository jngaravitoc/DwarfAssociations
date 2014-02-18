import numpy as np
import scipy as sp

data = np.loadtxt("../data/B64_WM5_10909_LG_7Mpc_2048/data.txt")

x = data[:,2]
y = data[:,3]
z = data[:,4]
m = data[:,8]
d = []

l = len(x)

for i in range(l):
    for j in range(l):
        dist = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2 + (z[i]-z[j])**2)
        d.append(dist)


f = open(str(distances.txt), 'w')
for i in range(len(d)):
    f.write(str(d[i]))
f.close()

