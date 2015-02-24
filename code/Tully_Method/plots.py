import numpy as np 
import matplotlib.pyplot as plt
import sys

filename = sys.argv[1] 
data =  np.loadtxt(filename)


x = data[:,0]
y = data[:,1]
z = data[:,2]
M = data[:,6]

Lx = max(x) - min(x)
Ly = max(y) - min(y)
Lz = max(z) - min(z)

Volume = Lx * Ly * Lz
density =  Volume/sum(M)

def mass_pictures(M):
	LogM = np.sort(np.log10(M))
	y = np.linspace(len(LogM), 1, len(LogM))
	plt.plot(LogM, y, c='k', linewidth=1.0)
	plt.yscale('log')
	plt.xlabel(r"$\rm{Log(M)}$")
	plt.ylabel(r"$\rm{Log(N(>M))}$")
	plt.xlim([min(np.log10(M)), max(np.log10(M))])
	plt.show()

mass_pictures(M)

