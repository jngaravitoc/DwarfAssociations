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
f2 = open("maxmembers.txt", "w")
fout = open("Results.txt", "w")
fout.write("# Group  Ndm Halos,  Ns Halos, DM Associations min, Stars Associations min, DM Associations max,  Stars Associations max \n")
f2.write("# group, mindm, maxdm, mins, maxs \n")
for i in range (53):
	snap_name = "Illustris_group_"+str(i)+".dat"
	x, y, z, vx, vy, vz, Mag =  loading_snapshot("../../data/Illustris/" + snap_name)
	x_stars, y_stars, z_stars, vx_stars, vy_stars, vz_stars = stars(x, y, z, vx, vy, vz, Mag)# Return the stars in the p	    
	N_DM = len(x)
	N_stars = len(x_stars)
	snap_fof_DM = "FOFDM" + snap_name
	snap_fof_stars = "FOF_stars" + snap_name
	# Running the FOF code
	fof(x, y, z, vx, vy, vz, N_DM, snap_fof_DM)
	fof(x_stars, y_stars, z_stars, vx_stars, vy_stars, vz_stars, N_stars, snap_fof_stars)
	#rint "Dm min = ",  NDM_min, "DM max = ", NDM_max, "Stars min = ", Nstars_min, "Stars max = ", Nstars_max 
	# Number of associations per groups
	# N_asso_dm_min.append(NDM_min)
        # N_asso_dm_max.append(NDM_max)
	# N_asso_stars_min.append(Nstars_min)
	# N_asso_stars_max.append(Nstars_max)
        # Numbre of memebers per association
	Nass, asso, mind, Nass_max, asso, maxd  =  N_associations(snap_fof_DM)
        NassDM_min += Nass
        NassDM_max += Nass_max
        Nass_stars, asso, mins , Nass_stars_max, asso, maxs =  N_associations(snap_fof_stars)
	NassStars_min += Nass_stars
        NassStars_max += Nass_stars_max
	# Removing the huge association
	print Nass_stars
	Nass.remove(mind)
	Nass_max.remove(maxd)
        Nass_stars.remove(mins)
	if (i==41):
		Nass_stars.remove(mins)
	        Nass_stars_max.remove(maxs)
	if (i==50):
                Nass_stars.remove(mins)
	Nass_stars_max.remove(maxs)
	f2.write(("%f \t %f \t %f \t %f \t %f \n")%(i, mind, maxd, mins, maxs))
	fout.write(("%d , %.0f , %.0f, %.0f, %.0f, %.0f, %.0f \n ")%(i, len(x), len(x_stars), len(Nass), len(Nass_stars), len(Nass_max), len(Nass_stars_max)))
	#rint "DM: ", Nass , Nass_max
	#rint "Stars: ", Nass_stars, Nass_stars_max
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
	plt.title(r"$NAsso\ LLmin =\ $" + str(len(Nass)) + r"$ NAsso\ LLmax =\ $" + str(len(Nass_max)), fontsize=18)
	plt.scatter(sigmax_min, sigmav_min, c='k', marker = "o", alpha=0.6, s=180, label='$LL\ =\ 526\ kpc$')
        plt.scatter(sigmax_max, sigmav_max, c='b', marker = "o", alpha=0.6, s=180, label='$LL\ =\ 724\ kpc$')
	plt.scatter(Xdisp_obs, Vdisp_obs, c='y', marker="*", s=180)
	plt.legend(fontsize=18)
	plt.xlim(-20,800)
	plt.ylim(-10, 120)
        plt.ylabel(r"$\sigma_v$", fontsize=25)
	plt.subplot(2, 2, 3)
	plt.scatter(sigmax_min, Nass,  c='k', alpha=0.6, marker = "o", s=180)
        plt.scatter(sigmax_max, Nass_max, c='b', marker = "o", alpha=0.6, s=180)
        plt.scatter(Xdisp_obs, N_obs, c='y', marker="*", s=180)
        plt.xlim(-20,800)
	plt.ylim(-10, 80)
	plt.ylabel(r"$Number\ of\ Members$", fontsize=25)
        plt.xlabel(r"$\sigma_x$", fontsize=25)
	plt.subplot(2, 2, 4)
        plt.scatter(sigmav_min, Nass, c='k', alpha=0.6,  marker = "o", s=180)
        plt.scatter(sigmav_max, Nass_max, c='b', marker = "o", alpha=0.6, s=180)
        plt.scatter(Vdisp_obs, N_obs, c='y', marker="*", s=180)
        plt.xlim(-10, 120)
	plt.ylim(-10, 80)
	plt.xlabel(r"$\sigma_v$", fontsize=25)
        #plt.show()
	plt.savefig("figures/Association" + str(i) + ".png")
        plt.close()

	#print len(sigmax_min), len(Nass)
        plt.figure(figsize=(15, 10))
        plt.subplot(2,2,1)
	plt.title(r"$NAsso\ LLmin\ =\ $" + str(len(Nass_stars)) + r"$   NAsso\ LLmin =\$"+ str(len(Nass_stars_max)), fontsize=18)
        plt.scatter(sigmax_min_s, sigmav_min_s, c='k', marker = "o", alpha=0.6, s=180,label='$LL\ =\ 526\ kpc$')
        plt.scatter(sigmax_max_s, sigmav_max_s, c='b', marker = "o", alpha=0.6, s=180,label='$LL\ =\ 724\ kpc$')
	plt.legend(fontsize=18)
        plt.scatter(Xdisp_obs, Vdisp_obs, c='y', marker="*", s=180)
	plt.xlim(-20, 600)
	plt.ylim(-10, 90)
	plt.ylabel(r"$\sigma_v$", fontsize=25)
        plt.subplot(2, 2, 3)
        plt.scatter(sigmax_min_s, Nass_stars, c='k', marker = "o", alpha=0.6, s=180)
        plt.scatter(sigmax_max_s, Nass_stars_max, c='b', marker = "o", alpha=0.6, s=180)
        plt.scatter(Xdisp_obs, N_obs,  c='y', marker="*", s=180)
	plt.xlim(-20, 600)
	plt.ylim(-10, 50)
	plt.ylabel(r"$Number\ of\ Members$", fontsize=25)
	plt.xlabel(r"$\sigma_x$", fontsize=25)
        plt.subplot(2, 2, 4)
        plt.scatter(sigmav_min_s, Nass_stars,  c='k',  marker = "o", alpha=0.6, s=180)
        plt.scatter(sigmav_max_s, Nass_stars_max ,marker = "o", c='b', alpha=0.6, s=180)
        plt.scatter(Vdisp_obs, N_obs,  c='y', marker="*", s=180)
	plt.xlim(-10, 90)
	plt.ylim(-10, 50)
	plt.xlabel(r"$\sigma_v$", fontsize=25)
        #plt.show()
        plt.savefig("figures/ObsAssociation" + str(i) + ".png")
        plt.close()

f2.close()	
f.close()
fout.close()
"""
XX, YY, ZZ = threedplot("FOFDMIllustris_group_0.dat")

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


print "Dark Matter"
print "------------"
print "N max", NDM_max
print "N min", NDM_min
print "Stars"
print "------------"
print "N max", Nstars_max
print "N min", Nstars_min
"""
