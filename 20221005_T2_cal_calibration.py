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

show_plot=0

#path = dir + '\\' + folder + '\\'
#folder_list=[ f.path for f in os.scandir(path) if f.is_dir() ]
num_of_subfolders=np.size(sub_folders)

input_power=[1.56, 1.16, 0.84, 0.60, 0.41] # unit:mW
pi_pulse_duation=[1.8e-6,2.2e-6,2.8e-6,3.2e-6,4.7e-6]
tau_0=[5e-6, 5e-6, 7e-6, 8e-6, 11e-6]

tau_step=2e-6
echo_reading_width=3e-6

ave=20
steps=20

path=dir + '\\' + folder + '\\' + sub_folders[0] + '\\'
file_list = os.listdir(path)
list_csv=natsorted([i for i in file_list if i.endswith('.CSV')])
file_size=np.shape(list_csv)
data_file_len=file_size[0]
read_example=pd.read_csv(os.path.join(path,list_csv[0]))
read_example=read_example.to_numpy()
row_of_data, column_of_data=np.shape(read_example)

tau_measured=np.empty([data_file_len,num_of_subfolders])
echo_area=np.empty([steps*ave,num_of_subfolders])
tau_plot=np.empty([steps,num_of_subfolders])
data_time=np.empty([num_of_subfolders,row_of_data,data_file_len])
data_trigger=np.empty([num_of_subfolders,row_of_data,data_file_len])
data_echo=np.empty([num_of_subfolders,row_of_data,data_file_len])
data_echo_corrected=np.empty([num_of_subfolders,row_of_data,data_file_len])
#data_background=np.empty([row_of_data,data_file_len])
data_background_ave=np.empty([steps*ave,num_of_subfolders])
Trigger_pos=np.empty([num_of_subfolders,2,data_file_len])
pulses_pos=np.empty([num_of_subfolders,4,data_file_len])

# Define the fitting fuction
def TPE(x,y0,T2):
    return y0*np.exp(-4*x/T2)

# Set up the time range for data processing
time_offset_left=10
time_offset_right=180

    # Values for finding the trigger, pi pulse, and pi/2 pulses
trigger_val = 1.5
pulses_val = 0.007

for index_0, file_0 in enumerate(sub_folders):
    path=dir + '\\' + folder + '\\' + file_0 + '\\'
    for index_1, file_1 in enumerate(list_csv):
        data=pd.read_csv(os.path.join(path,file_1))
        data=data.to_numpy()

        data_time[index_0,:,index_1]=data[:,0]
        data_time_1=data[:,0]

        data_trigger[index_0,:,index_1]=data[:,1]
        data_trigger_1=data[:,1]
    
        # Finding the trigger signal 
        mask1 = (data_trigger_1[:-1] < trigger_val) & (data_trigger_1[1:] > trigger_val)
        mask2 = (data_trigger_1[:-1] > trigger_val) & (data_trigger_1[1:] < trigger_val)
        Trigger_pos[index_0,:,index_1]=np.flatnonzero(mask1 | mask2)+1
    
        data_echo[index_0,:,index_1]=data[:,2]
        data_echo_1=data[:,2]
        data_background=data_echo_1[(int(Trigger_pos[index_0,1,index_1])+time_offset_right):]
        data_background_ave[index_1,index_0]=np.sum(data_background)/(len(data_background))

        #data_echo_corrected[:,index]=data_echo[:,index]-min(data_echo[:,index])
        data_echo_corrected[index_0,:,index_1]=data_echo[index_0,:,index_1]-data_background_ave[index_1,index_0]
        data_echo_corrected_1=data_echo_corrected[index_0,:,index_1]

        mask3 = (data_echo_corrected_1[:-1] < pulses_val) & (data_echo_corrected_1[1:] > pulses_val)
        mask4 = (data_echo_corrected_1[:-1] > pulses_val) & (data_echo_corrected_1[1:] < pulses_val)
        pulses_pos=np.flatnonzero(mask3 | mask4)+1

        tau_measured[index_1,index_0] = 1e6*np.abs(data_time_1[pulses_pos[0]]-data_time_1[pulses_pos[2]])+pi_pulse_duation[index_0]/4
        print(tau_measured[index_1,index_0])

        time_int=data_time[index_0,int(Trigger_pos[index_0,0,0])-time_offset_left:int(Trigger_pos[index_0,1,0])+time_offset_right,index_1]
        echo_int=data_echo_corrected[index_0,int(Trigger_pos[index_0,0,0])-time_offset_left:int(Trigger_pos[index_0,1,0])+time_offset_right,index_1]
        echo_area[index_1,index_0]=simpson(echo_int, time_int)
    
        if show_plot==1:
            fig1, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1.plot(data_time_1[int(pulses_pos[0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,index_1], data_trigger_1[int(pulses_pos[0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,index_1], 'g-')
            ax2.plot(data_time_1[int(pulses_pos[0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,index_1], data_echo_1[int(pulses_pos[0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,index_1], 'b-')
            plt.show()

#%%
for index_0 in range(num_of_subfolders):
    plt.figure()
    for index_2 in range(len(data_background_ave)):
        plt.plot(data_time[index_0, (int(Trigger_pos[index_0,1,index_2])+time_offset_right):,index_2],data_echo[index_0, (int(Trigger_pos[index_0,1,index_2])+time_offset_right):,index_2])
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude (V)')
        plt.title('Background')

# %%
data_echo_area=np.empty([steps,num_of_subfolders])
data_echo_area_ave=np.empty([ave,num_of_subfolders])
data_echo_SD_0=np.empty([ave,num_of_subfolders])
data_echo_SD=np.empty([steps,num_of_subfolders])
data_echo_error=np.empty([steps,num_of_subfolders])

for index_0 in range(num_of_subfolders):
    for ii in range(steps):
        jj=0
        while jj<ave:
            data_echo_area[jj,index_0]=echo_area[ii+(jj)*steps,index_0]
            jj=jj+1  
        data_echo_area_ave[ii,index_0]=np.sum(data_echo_area)/ave
    
        kk=0
        while kk<ave:
            data_echo_SD_0[kk,index_0]=np.square(echo_area[ii+(kk)*steps,index_0]-data_echo_area_ave[ii,index_0])
            kk=kk+1
            test=0
    
        data_echo_SD[ii,index_0]=np.sqrt(np.sum(data_echo_SD_0)/(ave-1))
        data_echo_error[ii,index_0]=data_echo_SD[ii,index_0]/np.sqrt(ave)
        
        data_time_plot=data_time[index_0,int(Trigger_pos[index_0,0,0])-time_offset_left:int(Trigger_pos[index_0,1,0])+time_offset_right,ii]
        data_trigger_plot=data_trigger[index_0,int(Trigger_pos[index_0,0,0])-time_offset_left:int(Trigger_pos[index_0,1,0])+time_offset_right,ii]
        tau_plot[ii,index_0]=tau_measured[ii,index_0]*1e-6

test=0
# %%
T2_fit=np.empty(num_of_subfolders)
T2_err_true=np.empty(num_of_subfolders)
for index_0 in range(num_of_subfolders):
    T2_fit_0,T2_err=curve_fit(TPE, tau_plot[:,index_0], data_echo_area_ave[:,index_0], p0=[1e-9,50e-6],sigma=data_echo_error[:,index_0])
    T2_fit[index_0]=T2_fit_0[1]
    T2_err_true_0=np.sqrt(np.diag(T2_err))
    T2_err_true[index_0]=T2_err_true_0[1]
    print('fitted T2 =', T2_fit[index_0]*1e6, 'us')
    print('fitted T2 error =', T2_err_true[index_0]*1e6, 'us')
# %%
