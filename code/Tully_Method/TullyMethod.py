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
  x = data[:,0]
  y = data[:,1]
  z = data[:,2]
  vx = data[:,3]
  vy = data[:,4]
  vz = data[:,5]
  M = data[:,6]


  return x, y, z, vx, vy, vz, M


def distances(filename):
    x, y, z, vx, vy, vz, M = reading(filename)
    r = []
    for i in range(len(x)):
        for j in range(len(y)):
             r.append(np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2)+(z[i]-z[j])**2)
            #print "distancia de: ", i, "a: ", j, " = ", d
    return x, y, z, vx, vy, vz, M, r

def force(filename): # ID es momentaneo
    x, y, z, vx, vy, vz, M, r = distances(filename)
    id_Mp = [] # Masa de la particula p
    id_Mq = [] # Masa de la particula q
    id_Xp = [] # Masa de la particula p
    id_Xq = [] # Masa de la particula q
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
                        id_Mp.append(M[p]) # Guardo las masas de las particulas
                        id_Mq.append(M[q])
                        id_Xp.append(x[p]) # Guardo la posicion en x de las particulas
                        id_Xq.append(x[q])
                        # Mass of possible New particle
                        if Mt > M[j]:
                            F.append(1/(r_cm**2/Mt))
                            MT.append(Mt)
                        else:
                            F.append(1/(r_cm**2/M[j]))
                            MT.append(M[j])
    index = np.where(F == min(F)) #Seleccion del minimo de la fuerza
    index =  index[0][1]
    #print idp[index], idq[index], MT[index] # Que pares de particulas minimizan la fuerza

    return id_Mp[index], id_Mq[index], id_Xp[index], id_Xq[index], MT[index], x, y, z, vx, vy, vz, M
    #return x[index], y[index], z[index], MT[index], ID, x, y, z, M


def new_particle(filename):
    id_mp, id_mq, id_xp, id_xq ,new_M, x, y, z, vx, vy, vz, M = force(filename)
    data = np.loadtxt(filename)
    #index = np.where
    indexp = np.where((M == id_mp) & (x == id_xp)) # esto lo hago para asegurar que solo seleccione una particula. Improbable misma particula con M y x iguales.
    indexq = np.where((M == id_mq) & (x == id_xq))
    print "Mass of p1 to merge", id_mp
    print "Mass of p2 to merge", id_mq
    print "Mass of new particle", new_M

    xp = x[indexp]
    yp = y[indexp]
    zp = z[indexp]
    xq = x[indexq]
    yq = y[indexq]
    zq = z[indexq]

    vx_p = vx[indexp]
    vy_p = vy[indexp]
    vz_p = vz[indexp]
    vx_q = vx[indexq]
    vy_q = vy[indexq]
    vz_q = vz[indexq]

    IDp = M[indexp]
    IDq = M[indexq]
    Mp = M[indexp]
    Mq = M[indexq]
    Mpq = Mp + Mq

    print "index", indexp, indexq
    print "Mpq = ", len(Mpq)
    print "Mp = ", len(Mp)
    print "Mq = ", len(Mq)
    #print Mp, xp, Mq, xq, Mpq

    xt = 1 / Mpq * (Mp*xp + Mq*xq)
    yt = 1 / Mpq * (Mp*yp + Mq*yq)
    zt = 1 / Mpq * (Mp*zp + Mq*zq)

    vxt = 1/ Mpq * (Mp*vx_p + Mq*vx_q)
    vyt = 1/ Mpq * (Mp*vy_p + Mq*vy_q)
    vzt = 1/ Mpq * (Mp*vz_p + Mq*vz_q)


    #print N+1, xt, yt, zt, new_M
    print "New x", xt, "New y", yt, "New z", zt
    print "----------------------------------------"

    data = np.delete(data, indexp, 0)
    data = np.delete(data, indexq, 0)

    #print new_M, xt
    f = open("data.dat", "w")
    for i in range(len(data)):
      f.write(("%f \t %f \t %f \t %f \t %f \t %f \t %f \n")%(data[i,0], data[i,1], data[i,2], data[i,3], data[i,4], data[i,5], data[i, 6]))
    f.write(("%f \t %f \t %f \t %f \t %f \t %f \t %f \n")%(xt, yt, zt, vxt, vyt, vzt, new_M))
    f.close()

    Volume =  (max(data[:,0]) - min(data[:,0])) * (max(data[:,1]) -min(data[:,1]) ) * (max(data[:,2]) - min(data[:,2]))
    total_mass = sum(data [:,4])
    density = total_mass / Volume
    #print Volume, "density", density
    return len(data), density



density = 0
MW-density = float(sys.argv[1])
while density < MW-density:
  LD, density = new_particle(filename)
  print "Numero de halos = ", LD, "Densidad del grupo",  density

# hashmap
