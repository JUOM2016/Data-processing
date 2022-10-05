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

for index , file in enumerate(sub_folders):
    path=dir + '\\' + folder + '\\' + file + '\\'
    file_list = os.listdir(path)
    list_csv=natsorted([i for i in file_list if i.endswith('.CSV')])
    file_size=np.shape(list_csv)
    data_file_len=file_size[0]
    read_example=pd.read_csv(os.path.join(path,list_csv[0]))
    read_example=read_example.to_numpy()
    row_of_data, column_of_data=np.shape(read_example)

    tau_measured=np.empty(data_file_len)
    echo_area=np.empty(steps*ave)
    tau_plot=np.empty(steps)
    data_time=np.empty([row_of_data,data_file_len])
    data_trigger=np.empty([row_of_data,data_file_len])
    data_echo=np.empty([row_of_data,data_file_len])
    data_echo_corrected=np.empty([row_of_data,data_file_len])
    #data_background=np.empty([row_of_data,data_file_len])
    data_background_ave=np.empty(steps*ave)
    Trigger_pos=np.empty([2,data_file_len])
    pulses_pos=np.empty([4,data_file_len])

    # Define the fitting fuction
    def TPE(x,y0,T2):
        return y0*np.exp(-4*x/T2)

    # Set up the time range for data processing
    time_offset_left=10
    time_offset_right=180

    # Values for finding the trigger, pi pulse, and pi/2 pulses
    trigger_val = 1.5
    pulses_val = 0.007
    test=0