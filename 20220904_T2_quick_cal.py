# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 20:32:28 2022

@author: wj2002
"""

import os
import numpy as np
import pandas as pd
from natsort import natsorted
import matplotlib.pyplot as plt
import sys

# Directory and folder for data
dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU\\20220902_Pr_YSO_T2_L'
folder = 'SHB_NosweepBB'

path = dir + '\\' + folder + '\\'
file_list = os.listdir(path)

# Listing all .csv files but not all data fies will be used in some cases
list_csv=natsorted([i for i in file_list if i.endswith('.CSV')])
file_size=np.shape(list_csv)
file_len=file_size[0]
intensity_max=np.zeros(file_len)
#time_output=np.zeros([3750,file_len])
#T2_data_selected_output=np.zeros([3750,file_len])

tau=6e-6
tau_step=4e-6
tau_values=np.zeros(file_len)

for index, file in enumerate(file_list):
    data=pd.read_csv(os.path.join(path,file))
    data=data.to_numpy()
    T2_data=data[:,2]
    time=data[:,0]
    tau_left=2*(tau+0.4e-6)-2.5e-6
    tau_right=2*(tau+0.4e-6)+4e-6
    difference_left = np.absolute(time-tau_left)
    difference_right = np.absolute(time-tau_right)
    time_left=np.argmin(difference_left)
    time_right=np.argmin(difference_right)
    T2_data_selected=T2_data[time_left:time_right]
    T2_data_corrected=T2_data_selected-min(T2_data_selected)
    intensity_max[index]=max(T2_data_corrected)
    #time_output[:,index]=time[time_left:time_right]
    #T2_data_selected_output[:,index]=T2_data_corrected
    tau_values[index]=tau
    
    plt.figure(1)
    plt.plot(time,T2_data)
    
    plt.figure(2)
    plt.plot(time[time_left:time_right],T2_data_corrected)
    tau=tau+tau_step
    test=0
    
plt.figure(3)
plt.plot(tau_values,intensity_max)
