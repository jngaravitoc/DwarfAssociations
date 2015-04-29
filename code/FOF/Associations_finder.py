import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import os
from functions import *

N_asso_dm_min = []
N_asso_dm_max = []
N_asso_stars_min = []
N_asso_stars_max = []
sigma_V = []
sigma_X = []


NassDM_min = []
NassDM_max = []
NassStars_min = []
NassStars_max = []

## Observed dispersions, data from table 2 of Tully et al 06
Vdisp_obs = [18, 36,  42, 11, 17, 35, 26, 37]#km/s
Xdisp_obs = [350, 280,  320, 300, 260, 380, 310, 570] #Kpc check the h factor
N_obs = [5, 6, 7, 4, 5, 3, 4, 4]

f = open("Nass.txt", "w")

for i in range (53):
	print "Grupo =", i
	snap_name = "Illustris_group_"+str(i)+".dat"
	x, y, z, vx, vy, vz, Mag =  loading_snapshot("../../data/Illustris/" + snap_name)
	x_stars, y_stars, z_stars, vx_stars, vy_stars, vz_stars = stars(x, y, z, vx, vy, vz, Mag)# Return the stars in the previous loaded snapshot
	#rint "NDM = ", len(x), "Nstars = ", len(x_stars)
	N_DM = len(x)
	N_stars = len(x_stars)
	snap_fof_DM = "FOFDM" + snap_name
	snap_fof_stars = "FOF_stars" + snap_name
	# Running the FOF code
	NDM_min, NDM_max = fof(x, y, z, vx, vy, vz, N_DM, snap_fof_DM)
	Nstars_min, Nstars_max = fof(x_stars, y_stars, z_stars, vx_stars, vy_stars, vz_stars, N_stars, snap_fof_stars)
	print "Dm min = ",  NDM_min, "DM max = ", NDM_max, "Stars min = ", Nstars_min, "Stars max = ", Nstars_max 
	# Number of associations per groups
	N_asso_dm_min.append(NDM_min)
        N_asso_dm_max.append(NDM_max)
	N_asso_stars_min.append(Nstars_min)
	N_asso_stars_max.append(Nstars_max)
        # Numbre of memebers per association
	Nass, asso =  N_associations("A_min"+snap_fof_DM)
        NassDM_min += Nass
	Nass_max, asso =  N_associations("A_max"+snap_fof_DM)
        NassDM_max += Nass_max
        Nass_stars, asso =  N_associations("A_min"+snap_fof_stars)
        NassStars_min += Nass_stars
        Nass_stars_max, asso =  N_associations("A_max"+snap_fof_stars)
        NassStars_max += Nass_stars_max
	# Computing the dispersions
	sigmax_min, sigmav_min, sigmax_max, sigmav_max = dispersiones(snap_fof_DM)
        sigmax_min_s, sigmav_min_s, sigmax_max_s, sigmav_max_s = dispersiones(snap_fof_stars)
	f.write(("%f \t %f \t %f \t %f \n")%(len(Nass), len(Nass_max), len(Nass_stars), len(Nass_stars_max)))
        #rint len(sigmax_min), len(Nass)	
	#######################################################
        #                                                     #
        #                   Making Plots                      #
        #                                                     #
        #######################################################
	plt.figure(figsize=(15, 10))
        plt.subplot(2, 2, 1)
	plt.title(str(len(Nass)) + "  " + str(len(Nass_max)))
	plt.scatter(sigmax_min, sigmav_min, c='r', marker = "H", alpha=1, s=180)
        plt.scatter(sigmax_max, sigmav_max, c='b', marker = "8", alpha=1, s=180)
	plt.scatter(Xdisp_obs, Vdisp_obs, c='y', marker="*", s=180)
        plt.ylabel(r"$\sigma_v$", fontsize=25)
	plt.subplot(2, 2, 3)
	plt.scatter(sigmax_min, Nass,  c='r', alpha=1, marker = "H", s=180)
        plt.scatter(sigmax_max, Nass_max, c='b', marker = "8", alpha=1, s=180)
        plt.scatter(Xdisp_obs, N_obs, c='y', marker="*", s=180)
        plt.ylabel(r"$Number\ of\ Members$", fontsize=25)
        plt.xlabel(r"$\sigma_x$", fontsize=25)
	plt.subplot(2, 2, 4)
        plt.scatter(sigmav_min, Nass, c='r', alpha=1,  marker = "H", s=180)
        plt.scatter(sigmav_max, Nass_max, c='b', marker = "8", alpha=1, s=180)
        plt.scatter(Vdisp_obs, N_obs, c='y', marker="*", s=180)
        plt.xlabel(r"$\sigma_v$", fontsize=25)
        #plt.show()
	plt.savefig("figures/Association" + str(i) + ".png")
        plt.close()

	#print len(sigmax_min), len(Nass)
        plt.figure(figsize=(15, 10))
        plt.subplot(2, 2, 1)
	plt.title(str(len(Nass_stars)) + "  "+ str(len(Nass_stars_max)))
        plt.scatter(sigmax_min_s, sigmav_min_s, c='r', marker = "H", alpha=1, s=180)
        plt.scatter(sigmax_max_s, sigmav_max_s, c='b', marker = "8", alpha=1, s=180)
        plt.scatter(Xdisp_obs, Vdisp_obs, c='y', marker="*", s=180)
	plt.ylabel(r"$\sigma_v$", fontsize=25)
        plt.subplot(2, 2, 3)
        plt.scatter(sigmax_min_s, Nass_stars, c='r', marker = "H", alpha=1, s=180)
        plt.scatter(sigmax_max_s, Nass_stars_max, c='b', marker = "8", alpha=1, s=180)
        plt.scatter(Xdisp_obs, N_obs,  c='y', marker="*", s=180)
	plt.ylabel(r"$Number\ of\ Members$", fontsize=25)
	plt.xlabel(r"$\sigma_x$", fontsize=25)
        plt.subplot(2, 2, 4)
        plt.scatter(sigmav_min_s, Nass_stars,  c='r',  marker = "H", alpha=1, s=180)
        plt.scatter(sigmav_max_s, Nass_stars_max ,marker = "8", c='b', alpha=1, s=180)
        plt.scatter(Vdisp_obs, N_obs,  c='y', marker="*", s=180)
	plt.xlabel(r"$\sigma_v$", fontsize=25)
        #plt.show()
        plt.savefig("figures/ObsAssociation" + str(i) + ".png")
        plt.close()
f.close()
plt.figure(figsize=(15, 10))
plt.subplot(1, 2, 1)
plt.hist(N_asso_dm_min, color='k', alpha=0.8, label=r"$\mathrm{LL = 526Mpc\ h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.hist(N_asso_dm_max, color='k', alpha=0.4, label=r"$\mathrm{LL = 724Mpc\ h^{-1}}$", bins=range(0, 20 + 1, 1))
plt.title(r"$\mathrm{Dark\ Associations}$", fontsize=25)
plt.xlabel(r"$\mathrm{Number\ of\ Associations\ per\ Group}$", fontsize=25)
plt.legend()
#lt.savefig("Nassociations_DM_min.png", bbox_inches="tight")


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
