import numpy as np
from array import array
import sys

# TO DO:
# 1. Fix problem of the id, possile solution choose by Position
# 3. check if NEW_mas is correct

filename = "data.dat"
#filename2  = sys.argv[1]
N = 99 # Numero de lineas inicial

def reading(filename):
  data = np.loadtxt(filename)
  ID = data[:,0]
  x = data[:,1]
  y = data[:,2]
  z = data[:,3]
  M = data[:,4]


  return ID, x, y, z, M


def distances(filename):
    ID, x, y, z, M = reading(filename)
    r = []
    for i in range(len(x)):
        for j in range(len(y)):
             r.append(np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2)+(z[i]-z[j])**2)
            #print "distancia de: ", i, "a: ", j, " = ", d
    return ID, x, y, z, M, r

def force(filename):
    ID, x, y, z, M, r = distances(filename)
    idp = []
    idq = []
    N = len(x)
    R = []
    F = []
    MT = []
    #print M, r
    for p in range(N):
       for q in range(N):
            if p!=q:
                for j in range(N):
                    if ((j!=p) & (j!=q)):
                        Mt = M[p] + M[q]
                        r_cm = np.sqrt( (M[p] / (Mt) * r[j+p*N]**2 )+ (M[q] / (Mt) * r[j + q*N]**2) - (M[p]*M[q] / Mt**2 * r[q+p*N]**2) )
                        R.append(r_cm)
                        idp.append(M[p])# Ac poner seleccion p
                        idq.append(M[q])
                        if Mt > M[j]:
                            F.append(1/(r_cm**2/Mt))
                            MT.append(Mt)
                        else:
                            F.append(1/(r_cm**2/M[j]))
                            MT.append(M[j])
    index = np.where(F == min(F))
    index =  index[0][1]
    print idp[index], idq[index], MT[index]

    return idp[index], idq[index], MT[index], x, y, z, M
    #return x[index], y[index], z[index], MT[index], ID, x, y, z, M


def new_particle(filename):
    id_p, id_q, new_M, x, y, z, M = force(filename)
    data = np.loadtxt(filename)
    #index = np.where
    indexp = np.where(M == id_p)
    indexq = np.where(M == id_q)
    print "1p to merg", id_p
    print "2p to merge", id_q
    print "New mass of new particle", new_M
    xp = x[indexp]
    yp = y[indexp]
    zp = z[indexp]
    xq = x[indexq]
    yq = y[indexq]
    zq = z[indexq]
    IDp = M[indexp]
    IDq = M[indexq]
    Mp = M[indexp]
    Mq = M[indexq]
    Mpq = Mp + Mq
    #print Mp, xp, Mq, xq, Mpq
    xt = 1 / Mpq * (Mp*xp + Mq*xq)
    yt = 1 / Mpq * (Mp*yp + Mq*yq)
    zt = 1 / Mpq * (Mp*zp + Mq*zq)
    #print N+1, xt, yt, zt, new_M
    print "New x", xt, "New y", yt, "New z", zt
    #X = np.array([N, xt, yt, zt, new_M])
    data = np.delete(data, indexp, 0)
    data = np.delete(data, indexq, 0)

    print new_M, xt
    f = open("data.dat", "w")
    for i in range(len(data)):
      f.write(("%f \t %f \t %f \t %f \t %f \n")%(data[i,0], data[i,1], data[i,2], data[i,3], data[i,4]))
    f.write(("%f \t %f \t %f \t %f \t %f \n")%(N+1, xt, yt, zt, new_M))
    f.close()

    return len(data)
LD = 100
merging = float(sys.argv[1])
while LD>merging:
  LD = new_particle(filename)
  print LD

# hashmap
