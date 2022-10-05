"""
Author: Wei Jiang
Date: 2022/10/05 11:50am
"""
#%%
import os
import numpy as np
import pandas as pd
from natsort import natsorted
import matplotlib.pyplot as plt
import sys
from scipy.integrate import simpson
from scipy.optimize import curve_fit

dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU'
folder = '20220921_Pr_YSO_T2_L'
sub_folders = ['T292104','T292105','T292106','T292107','T292108']

#path = dir + '\\' + folder + '\\'
#folder_list=[ f.path for f in os.scandir(path) if f.is_dir() ]
#num_of_folders=np.size(folder_list)

input_power=[1.56, 1.16, 0.84, 0.60, 0.41] # unit:mW
pi_pulse_duation=[1.8e-6,2.2e-6,2.8e-6,3.2e-6,4.7e-6]
tau_0=[5e-6, 5e-6, 7e-6, 8e-6, 11e-6]

tau_step=2e-6
echo_reading_width=3e-6

ave=20
steps=20

for index in enumerate(sub_folders):
    path=dir + '\\' + folder + '\\' + sub_folders[index] + '\\'

    test=0