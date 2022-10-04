# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 21:58:19 2022

@author: wj2002
"""
#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import simpson


# Directory and folder for data
dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU'
folder = '20220928_Pr_YSO_AFC'

path = dir + '\\' + folder + '\\'

data_file='ECH92805'
ref_file ='IN92807'

read_data=pd.read_csv(os.path.join(path,data_file +'.'+'csv'))
read_ref=pd.read_csv(os.path.join(path,ref_file +'.'+'csv'))

data=read_data.to_numpy()
data_trigger=data[:,1]
ref=read_ref.to_numpy()
ref_trigger=ref[:,1]

figure,ax=plt.subplots()
ax1 = ax.twinx()
ax.plot(data[:,0],data[:,2],'r')
ax1.plot(data[:,0],data[:,3],'b')
plt.show()

figure,ax=plt.subplots()
ax1 = ax.twinx()
ax.plot(ref[:,0],ref[:,2],'r')
ax1.plot(ref[:,0],ref[:,3],'b')
plt.show()

#%%
trigger_val = 1.5

mask1 = (data_trigger[:-1] < trigger_val) & (data_trigger[1:] > trigger_val)
mask2 = (data_trigger[:-1] > trigger_val) & (data_trigger[1:] < trigger_val)
data_trigger_pos=np.flatnonzero(mask1 | mask2)+1

mask1 = (ref_trigger[:-1] < trigger_val) & (ref_trigger[1:] > trigger_val)
mask2 = (ref_trigger[:-1] > trigger_val) & (ref_trigger[1:] < trigger_val)
ref_trigger_pos=np.flatnonzero(mask1 | mask2)+1

offset=15000
offset_1=5000
data_time=data[int(data_trigger_pos[0]):int(data_trigger_pos[0])+offset,0]
ref_time=ref[int(ref_trigger_pos[0]):int(ref_trigger_pos[0])+offset_1,0]
data_echo=data[int(data_trigger_pos[0]):int(data_trigger_pos[0])+offset,2]
ref_echo=ref[int(ref_trigger_pos[0]):int(ref_trigger_pos[0])+offset_1,2]
data_reflection_signal=data[int(data_trigger_pos[0]):int(data_trigger_pos[0])+offset,3]
ref_reflection_signal=ref[int(ref_trigger_pos[0]):int(ref_trigger_pos[0])+offset_1,3]

figure,ax=plt.subplots()
ax1 = ax.twinx()
ax.plot(data_time,data_echo,'r')
ax1.plot(data_time,data_reflection_signal,'b')
plt.show()

figure,ax=plt.subplots()
ax1 = ax.twinx()
ax.plot(ref_time,ref_echo,'r')
ax1.plot(ref_time,ref_reflection_signal,'b')
plt.show()

#%%
data_background=data[int(data_trigger_pos[0]+offset):int(data_trigger_pos[0])+offset+2000,2]
ref_background =ref[int(ref_trigger_pos[0]+offset_1):int(ref_trigger_pos[0])+offset_1+2000,2]

data_background_ave=np.sum(data_background)/(len(data_background))
ref_background_ave=np.sum(ref_background)/(len(ref_background))

ref_pulse_left=0.6e-6
ref_pulse_right=1.8e-6
ref_pulse_left_pos=index = np.argmin(np.abs(ref[:,0]-ref_pulse_left))
ref_pulse_right_pos=index = np.argmin(np.abs(ref[:,0]-ref_pulse_right))
ref_pulse_time_int=ref[ref_pulse_left_pos:ref_pulse_right_pos,0]
ref_pulse_int=ref[ref_pulse_left_pos:ref_pulse_right_pos,2]

figure,ax=plt.subplots()
ax.plot(ref_pulse_time_int,ref_pulse_int,'r')
plt.show()

ref_pulse_int_corrected=ref_pulse_int-ref_background_ave
ref_input_area=simpson(ref_pulse_int_corrected,ref_pulse_time_int)

data_echo_left=4.7e-6
data_echo_right=6e-6
data_echo_left_pos=index = np.argmin(np.abs(data[:,0]-data_echo_left))
data_echo_right_pos=index = np.argmin(np.abs(data[:,0]-data_echo_right))
data_echo_time_int=data[data_echo_left_pos:data_echo_right_pos,0]
data_echo_int=data[data_echo_left_pos:data_echo_right_pos,2]

figure,ax=plt.subplots()
ax.plot(data_echo_time_int,data_echo_int,'r')
plt.show()

data_echo_int_corrected=data_echo_int-data_background_ave
AFC_echo_area=simpson(data_echo_int_corrected,data_echo_time_int)

AFC_efficiency=100*AFC_echo_area/ref_input_area

print('AFC efficiency is', AFC_efficiency,'%')
# %%
