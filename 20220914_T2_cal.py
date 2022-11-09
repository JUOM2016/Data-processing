# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 10:47:33 2022

@author: Wei Jiang

This codes are used to calculate the T2. In the codes, the 
average curves of each echo are calculated firstly and then calculate the 
areas of all echo.
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

# Directory and folder for data
dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU\\20220921_Pr_YSO_T2_L'
folder = 'T292104'

input_power=1.16 # unit:mW
pi_pulse_duation=2.2e-6
tau_0=5e-6

tau_step=2e-6
echo_reading_width=3e-6

ave=20
steps=20

path = dir + '\\' + folder + '\\'
file_list = os.listdir(path)

show_individual_plot=0
show_average_plot=1

# Listing all .csv files but not all data fies will be used in some cases
list_csv=natsorted([i for i in file_list if i.endswith('.CSV')])
file_size=np.shape(list_csv)
data_file_len=file_size[0]

read_example=pd.read_csv(os.path.join(path,list_csv[0]))
read_example=read_example.to_numpy()
row_of_data, column_of_data=np.shape(read_example)

tau_measured=np.empty(data_file_len)
echo_area=np.empty(steps)
tau_plot=np.empty(steps)
data_time=np.empty([row_of_data,data_file_len])
data_trigger=np.empty([row_of_data,data_file_len])
data_echo=np.empty([row_of_data,data_file_len])
data_echo_corrected=np.empty([row_of_data,data_file_len])
data_background_ave=np.empty(steps*ave)
Trigger_pos=np.empty([2,data_file_len])
pulses_pos=np.empty([4,data_file_len])

def TPE(x,y0,T2):
    return y0*np.exp(-4*x/T2)

time_offset_left=10
time_offset_right=180
trigger_val = 1.5   
pulses_val = 0.007 

for index, file in enumerate(list_csv):
    data=pd.read_csv(os.path.join(path,file))
    data=data.to_numpy()
    
    data_time[:,index]=data[:,0]
    data_time_1=data[:,0]
    
    data_trigger[:,index]=data[:,1]
    data_trigger_1=data[:,1]
    
    mask1 = (data_trigger_1[:-1] < trigger_val) & (data_trigger_1[1:] > trigger_val)
    mask2 = (data_trigger_1[:-1] > trigger_val) & (data_trigger_1[1:] < trigger_val)
    Trigger_pos[:,index]=np.flatnonzero(mask1 | mask2)+1
    
    data_echo[:,index]=data[:,2]
    data_echo_1=data[:,2]
    data_background=data_echo[(int(Trigger_pos[1,index])+time_offset_right):,index]
    data_background_ave[index]=np.sum(data_background)/(len(data_background))
    
    #data_echo_corrected[:,index]=data_echo[:,index]-min(data_echo[:,index])
    data_echo_corrected[:,index]=data_echo[:,index]-data_background_ave[index]
    data_echo_corrected_1=data_echo_corrected[:,index]
    
    mask3 = (data_echo_corrected_1[:-1] < pulses_val) & (data_echo_corrected_1[1:] > pulses_val)
    mask4 = (data_echo_corrected_1[:-1] > pulses_val) & (data_echo_corrected_1[1:] < pulses_val)
    pulses_pos=np.flatnonzero(mask3 | mask4)+1
    
    tau_measured[index] = 1e6*np.abs(data_time_1[pulses_pos[0]]-data_time_1[pulses_pos[2]])+pi_pulse_duation/4
    print(tau_measured[index])
    

    if show_individual_plot==1:
        fig1, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(data_time[int(pulses_pos[0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,index], data_trigger[int(pulses_pos[0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,index], 'g-')
        ax2.plot(data_time[int(pulses_pos[0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,index], data_echo[int(pulses_pos[0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,index], 'b-')
        plt.show()

plt.figure()
for index in range(len(data_background_ave)):
    plt.plot(data_time[(int(Trigger_pos[1,index])+time_offset_right):,index],data_echo[(int(Trigger_pos[1,index])+time_offset_right):,index])
    #plt.show()

data_len_echo=int((Trigger_pos[1,0]+time_offset_right)-(Trigger_pos[0,0]-time_offset_left))
data_echo_sum=np.empty([data_len_echo,steps])
data_echo_ave=np.empty([data_len_echo,steps])
#%%
for ii in range(steps):
    data_echo_first=data_echo_corrected[int(Trigger_pos[0,0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,ii]
    #data_echo_first=data_echo[:,ii]
    jj=1
    while jj<ave:
        data_echo_first=data_echo_first+data_echo_corrected[int(Trigger_pos[0,0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,ii+(jj)*steps]
        #data_echo_first=data_echo_first+data_echo[:,ii+(jj)*steps]

        jj=jj+1
    data_echo_sum[:,ii]=data_echo_first
    #data_echo_ave[:,ii]=(data_echo_sum[:,ii]-min(data_echo_sum[:,ii]))/ave
    data_echo_ave[:,ii]=data_echo_sum[:,ii]/ave
    data_time_plot=data_time[int(Trigger_pos[0,0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,ii]
    data_trigger_plot=data_trigger[int(Trigger_pos[0,0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,ii]
    tau_plot[ii]=tau_measured[ii]*1e-6
    
    if show_average_plot==1:
        
        fig2,ax3 = plt.subplots()
        ax4 = ax3.twinx()
        ax3.plot(data_time_plot, data_echo_ave[:,ii], 'r-',label="{}".format(tau_plot[ii]*1e6)+' us')
        ax4.plot(data_time_plot, data_trigger_plot, 'k-')
        ax3.legend(handlelength=2)
        plt.show()
    
    time_int=data_time[int(Trigger_pos[0,0])-time_offset_left:int(Trigger_pos[1,0])+time_offset_right,ii]
    echo_int=data_echo_ave[:,ii]
    echo_area[ii]=simpson(echo_int, time_int)
    
    
    test=1

T2_fit,T2_err=curve_fit(TPE, tau_plot, echo_area, p0=(1e-9, 40e-6))
T2_err_true=np.sqrt(np.diag(T2_err))
print('fitted T2 =', T2_fit[1]*1e6, 'us')
print('fitted T2 error =', T2_err_true[1]*1e6, 'us')

fig, ax=plt.subplots()
ax.errorbar(tau_plot*1e6, echo_area,fmt="sr")
xx=np.arange(4e-6,70e-6,10e-7)
T2_fit_curve=T2_fit[0]*np.exp(-4*xx/T2_fit[1])
ax.plot(xx*1e6,T2_fit_curve,'b--',label='\u03C0 pulse duration='+"{:.2f}".format(pi_pulse_duation*1e6)+' \u03BCs')
ax.legend(handlelength=2)
ax.set_xlabel('\u03C4 (\u03BCs)')
ax.set_ylabel('Echo area')
ax.annotate('Input power ='+"{:.2f}".format(input_power)+' mW',
            xy=(1, 0.5), xycoords='axes fraction',
            xytext=(-20, 20), textcoords='offset pixels',
            horizontalalignment='right',
            verticalalignment='bottom')
ax.annotate('Fitted T2 ='+"{:.2f}".format(T2_fit[1]*1e6)+' \u03BCs',
            xy=(1, 0.4), xycoords='axes fraction',
            xytext=(-20, 20), textcoords='offset pixels',
            horizontalalignment='right',
            verticalalignment='bottom')
ax.annotate('Fitted T2 error ='+"{:.2f}".format(T2_err_true[1]*1e6)+' \u03BCs',
            xy=(1, 0.3), xycoords='axes fraction',
            xytext=(-20, 20), textcoords='offset pixels',
            horizontalalignment='right',
            verticalalignment='bottom')
plt.show()
