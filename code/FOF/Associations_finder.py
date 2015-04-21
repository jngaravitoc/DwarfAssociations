import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os
from functions import *

N_asso_dm_min = []
N_asso_dm_max = []
N_asso_stars_min = []
N_asso_stars_max = []

NassDM_min = []
NassDM_max = []
NassStars_min = []
NassDtars_max = []

for i in range (53):
	snap_name = "Illustris_group_"+str(i)+".dat"
	x, y, z, vx, vy, vz, Mag =  loading_snapshot("../../data/Illustris/" + snap_name)
	#print Mag
	x_stars, y_stars, z_stars, vx_stars, vy_stars, vz_stars = stars(x, y, z, vx, vy, vz, Mag)
	#print "NDM = ", len(x), "Nstars = ", len(x_stars)
	N_DM = len(x)
	N_stars = len(x_stars)
	snap_fof_DM = "FOFDM" + snap_name
	snap_fof_stars = "FOF_stars" + snap_name
	NDM_min, NDM_max = fof(x, y, z, vx, vy, vz, N_DM, snap_fof_DM)
	Nstars_min, Nstars_max = fof(x_stars, y_stars, z_stars, vx_stars, vy_stars, vz_stars, N_stars, snap_fof_stars)
	N_asso_dm_min.append(NDM_min)
        N_asso_dm_max.append(NDM_max)
	N_asso_stars_min.append(Nstars_min)
	N_asso_stars_max.append(Nstars_max)
        
	Nass, asso =  N_associations("A_min"+snap_fof_DM)
        NassDM_min += Nass
plt.figure(figsize=(15, 10))
plt.subplot(1, 2, 1)
plt.hist(N_asso_dm_min, color='k', alpha=0.6, label=r"$\mathrm{LL = 526Mpc\ h^{-1}}$")
plt.hist(N_asso_dm_max, color='orange', alpha=0.6, label=r"$\mathrm{LL = 724Mpc\ h^{-1}}$")
plt.title(r"$\mathrm{Dark\ Associations}$", fontsize=25)
plt.xlabel(r"$\mathrm{Number\ of\ Associations\ per\ LG}$", fontsize=25)
plt.legend()
#plt.savefig("Nassociations_DM_min.png", bbox_inches="tight")


plt.subplot(1, 2, 2)
plt.hist(N_asso_stars_min, color='purple', alpha=0.6, label=r"$\mathrm{LL = 526Mpc\ h^{-1}}$")
plt.hist(N_asso_stars_max, color='blue', alpha=0.6, label=r"$\mathrm{LL = 724Mpc h^{-1}}$")
plt.title(r"$\mathrm{Observable\ Associations}$", fontsize=25)
plt.xlabel(r"$\mathrm{Number\ of\ Associations\ per\ LG}$", fontsize=25)
plt.legend()
plt.savefig("Nassociations.png", bbox_inches="tight")
plt.show()
plt.close()


plt.hist(NassDM_min, bins=20)
plt.show()
plt.close()

"""
print "Dark Matter"
print "------------"
print "N max", NDM_max
print "N min", NDM_min
print "Stars"
print "------------"
print "N max", Nstars_max
print "N min", Nstars_min
"""
