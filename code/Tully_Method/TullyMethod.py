import numpy as np
from array import array
import sys

filename = "HRbcku.txt"
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
                        idp.append(p)
                        idq.append(q)
                        if Mt > M[j]:
                            F.append(1/(r_cm**2/Mt))
                            MT.append(Mt)
                        elif M[j] > Mt:
                            F.append(1/(r_cm**2/M[j]))
                            MT.append(M[j])
    index = np.where(F == min(F))
    index =  index[0][1]

    return idp[index], idq[index], MT[index], ID, x, y, z, M

def new_particle(filename):
    id_p, id_q, new_M, ID, x, y, z, M = force(filename)
    data = np.loadtxt(filename)
    indexp = np.where(ID == id_p)
    indexq = np.where(ID == id_q)
    xp = x[indexp]
    yp = y[indexp]
    zp = z[indexp]
    xq = x[indexq]
    yq = y[indexq]
    zq = z[indexq]
    IDp = ID[indexp]
    IDq = ID[indexq]
    Mp = M[indexp]
    Mq = M[indexq]
    Mpq = Mp + Mq
    xt = 1 / Mpq * (Mp*xp + Mq*xq)
    yt = 1 / Mpq * (Mp*yp + Mq*yq)
    zt = 1 / Mpq * (Mp*zp + Mq*zq)
    X = np.array([N, xt, yt, zt, new_M])
    if IDp > IDq:
      data = np.delete(data, IDp, 0)
      data = np.delete(data, IDq, 0)
    else:
      data = np.delete(data, IDq, 0)
      data = np.delete(data, IDp, 0)

    np.insert(data, N, X)

    return  data, X
data, X = new_particle(filename)
print X
print data
