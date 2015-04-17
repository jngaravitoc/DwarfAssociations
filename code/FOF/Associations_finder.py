import numpy as np
import scipy as sp
import os
from functions import *

snap_name = "Illustris_group_0.dat"
x, y, z, vx, vy, vz, Mag =  loading_snapshot("../../data/Illustris/" + snap_name)
x_stars, y_stars, z_stars, vx_stars, vy_stars, vz_stars = stars(x, y, z, vx, vy, vz, Mag)

N_DM = len(x)
N_stars = len(x_stars)

snap_fof_DM = "FOFDM" + snap_name
snap_fof_stars = "FOF_stars" + snap_name
fof(x, y, z, vx, vy, vz, N_DM, snap_fof_DM)
fof_stars(x_stars, y_stars, z_stars, vx_stars, vy_stars, vz_stars, N_stars, snap_fof_stars)

