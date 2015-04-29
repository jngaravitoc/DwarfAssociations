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
NassStars_max = []

## Observed dispersions, data from table 2 of Tully et al 06
Vdisp_obs = [18, 36,  42, 11, 17, 35, 26, 37]#km/s
Xdisp_obs = [350, 280,  320, 300, 260, 380, 310, 570] #Kpc check the h factor
N_obs = [5, 6, 7, 4, 5, 3, 4, 4]

for i in range (53):
	print "Grupo =", i
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
	Nass_max, asso =  N_associations("A_max"+snap_fof_DM)
        NassDM_max += Nass_max
        Nass_stars, asso =  N_associations("A_min"+snap_fof_stars)
        NassStars_min += Nass_stars
        Nass_stars_max, asso =  N_associations("A_max"+snap_fof_stars)
        NassStars_max += Nass_stars_max
	sigmax_min, sigmav_min, sigmax_max, sigmav_max = dispersiones(snap_fof_DM)
        sigmax_min_s, sigmav_min_s, sigmax_max_s, sigmav_max_s = dispersiones(snap_fof_stars)

        #rint len(sigmax_min), len(Nass)	
	plt.figure(figsize=(15, 10))
        plt.subplot(2, 2, 1)
	plt.scatter(sigmax_min, sigmav_min, c='k', alpha=0.5, s=180)
        plt.scatter(sigmax_max, sigmav_max, c='k', alpha=1, s=180)
	plt.scatter(Xdisp_obs, Vdisp_obs, c='y', marker="*", s=180)
	plt.subplot(2, 2, 3)
	plt.scatter(Nass, sigmax_min, c='k', alpha=0.5, s=180)
        plt.scatter(Nass_max, sigmax_max, c='k', alpha=1, s=180)
        plt.scatter(N_obs, Xdisp_obs,c='y', marker="*", s=180)
        plt.subplot(2, 2, 4)
        plt.scatter(Nass, sigmav_min, c='k', alpha=0.5, s=180)
        plt.scatter(Nass_max, sigmav_max, c='k', alpha=1, s=180)
        plt.scatter(N_obs, Vdisp_obs, c='y', marker="*", s=180)
        plt.show()
        plt.close()

	#print len(sigmax_min), len(Nass)
        plt.figure(figsize=(15, 10))
        plt.subplot(2, 2, 1)
        plt.scatter(sigmax_min_s, sigmav_min_s, c='r', alpha=0.5, s=180)
        plt.scatter(sigmax_max_s, sigmav_max_s, c='b', alpha=1, s=180)
        plt.scatter(Xdisp_obs, Vdisp_obs, c='y', marker="*", s=180)
        plt.subplot(2, 2, 3)
        plt.scatter(Nass_stars, sigmax_min_s, c='k', alpha=0.5, s=180)
        plt.scatter(Nass_stars_max, sigmax_max_s, c='k', alpha=1, s=180)
        plt.scatter(N_obs, Xdisp_obs,c='y', marker="*", s=180)
        plt.subplot(2, 2, 4)
        plt.scatter(Nass_stars, sigmav_min_s, c='k', alpha=0.5, s=180)
        plt.scatter(Nass_stars_max, sigmav_max_s, c='k', alpha=1, s=180)
        plt.scatter(N_obs, Vdisp_obs, c='y', marker="*", s=180)
        plt.show()
        plt.close()

plt.figure(figsize=(15, 10))
plt.subplot(1, 2, 1)
plt.hist(N_asso_dm_min, color='k', alpha=0.8, label=r"$\mathrm{LL = 526Mpc\ h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.hist(N_asso_dm_max, color='k', alpha=0.4, label=r"$\mathrm{LL = 724Mpc\ h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.title(r"$\mathrm{Dark\ Associations}$", fontsize=25)
plt.xlabel(r"$\mathrm{Number\ of\ Associations\ per\ Group}$", fontsize=25)
plt.legend()
#plt.savefig("Nassociations_DM_min.png", bbox_inches="tight")


plt.subplot(1, 2, 2)
plt.hist(N_asso_stars_min, color='purple', alpha=0.6, label=r"$\mathrm{LL = 526Mpc\ h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.hist(N_asso_stars_max, color='blue', alpha=0.6, label=r"$\mathrm{LL = 724Mpc h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.title(r"$\mathrm{Observable\ Associations}$", fontsize=25)
plt.xlabel(r"$\mathrm{Number\ of\ Associations\ per\ Group}$", fontsize=25)
plt.legend()
plt.savefig("Nassociations.png", bbox_inches="tight")
#plt.show()
plt.close()

plt.figure(figsize=(15, 10))
plt.subplot(1, 2, 1)
plt.hist(NassDM_min, color="k", alpha=0.8, label=r"$\mathrm{LL = 526Mpc\ h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.hist(NassDM_max, color="k", alpha=0.4, label=r"$\mathrm{LL = 724Mpc h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.xlabel(r"$\mathrm{Number\ of\ members\ per\ Association}$", fontsize=25)
plt.xlim([0, 20])
plt.ylim([0, 250])
plt.legend()

plt.subplot(1, 2, 2)
plt.hist(NassStars_min, color="purple", alpha=0.6, label=r"$\mathrm{LL = 526Mpc\ h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.hist(NassStars_max, color="blue", alpha=0.6, label=r"$\mathrm{LL = 724Mpc h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.xlabel(r"$\mathrm{Number\ of\ members\ per\ Association}$", fontsize=25)
plt.xlim([0, 20])
plt.ylim([0, 250])
plt.legend()
plt.savefig("Nmembersassociations.png", bbox_inches="tight")
#plt.show()
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
