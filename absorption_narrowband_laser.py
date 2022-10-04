"""
Created on Wed May 18 22:56:45 2022

@author: wj2002-Wei Jiang

The program is used to deal with the data of absorption using narrowband laser;
"""

import os
import numpy as np
import pandas as pd
from natsort import natsorted
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
from tkinter import filedialog as fd
from scipy import signal

# directory and folder for raw data
dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU'
folder = '20220527_606_laser_fluctuation_test'

path = dir + '\\' + folder + '\\'
file_list = os.listdir(path)

#filename=fd.askopenfiles()
#file = open(filename,'r')
#  file names (transmitted signal with the crystal) and reference file names (transmitted signals without crystal)
#file_name=['ABS51901','ABS51902','ABS51903','ABS51904','ABS51905','ABS51906']
#ref_name= ['ABS51907','ABS51908','ABS51909','ABS51910','ABS51911','ABS51912']
file_name=['VPF52701','VPF52702','VPF52703','VPF52704','VPF52705','VPF52706']
ref_name= ['VPF52707','VPF52708','VPF52709','VPF52710','VPF52711','VPF52712']
# angles of half-wave plate to change the input laser polarisations
#angle_of_half_waveplate=['188$^\circ$ (D2)','180$^\circ$','170$^\circ$','160$^\circ$','150$^\circ$','143$^\circ$ (D1)'] # for 1550 nm laser
angle_of_half_waveplate=['87$^\circ$ (D2)','90$^\circ$','100$^\circ$','110$^\circ$','120$^\circ$','132$^\circ$ (D1)'] #for 606 nm laser

#extract data of the time-scale and Piezo signal
num_files=len(file_name)
read_example=pd.read_csv(os.path.join(path,file_name[0] +'.'+'csv'))
example=read_example.to_numpy()
time_scale=example[:,0]
piezo_signal=example[:,1]

#create arrays for data processing 
[length_of_data,column_of_data]=np.shape(example)
absorption=np.empty([length_of_data,num_files])
absorption_corrected=np.empty([length_of_data,num_files])
laser_fluc_data=np.empty([length_of_data,num_files])
laser_fluc_data_corrected=np.empty([length_of_data,num_files])
laser_fluc_of_ref=np.empty([length_of_data,num_files])
laser_fluc_of_ref_corrected=np.empty([length_of_data,num_files])
data=np.empty([num_files,length_of_data,column_of_data])
transmission_data=np.empty([length_of_data,num_files])
transmission_data_corrected=np.empty([length_of_data,num_files])
ref_data=np.empty([num_files,length_of_data,column_of_data])
transmission_ref_data=np.empty([length_of_data,num_files])
transmission_ref_data_corrected=np.empty([length_of_data,num_files])
difference=np.empty([num_files])
ref_difference=np.empty([num_files])
absorption_max=np.zeros([num_files])
location_absorption_max=np.zeros([num_files])

#extract the raw data
for index,file in enumerate(file_name):
    ref=ref_name[index]
    read_data=pd.read_csv(os.path.join(path,file +'.'+'csv'))
    data[index,:,:]=read_data.to_numpy()
    transmission_data[:,index]=data[index,:,3] #save the data of transmitted signals with the crystal
    read_ref=pd.read_csv(os.path.join(path,ref +'.'+'csv'))
    ref_data[index,:,:]=read_ref.to_numpy()
    transmission_ref_data[:,index]=ref_data[index,:,3] #save the data of transmitted reference signals without the crystal
    laser_fluc_data[:,index]=data[index,:,2] #save the laser power fluctuations (with the crystal) on the other beam path of the PBS
    laser_fluc_of_ref[:,index]=ref_data[index,:,2] #save the laser power fluctuations (with the crystal) on the other beam path from the PBS
    absorption[:,index]=np.log(transmission_ref_data[:,index]/transmission_data[:,index]) #calculate the OD based on the raw data
    
laser_power_max=np.amax(laser_fluc_data) #find out the maximum laser power from the other beam path of the PBS for calibration 
location = np.where(laser_fluc_data == laser_power_max)

#calibrate the transmitted signals based on the laser power references from the other beam path of the PBS
for ii in range(num_files):
    array_max=np.amax(laser_fluc_data[:,ii]) #find out the maximum laser power of each laser polarisation (with the crystal)
    difference[ii]=laser_power_max-array_max #calculate the difference of laser maximal of each laser polarisation with the maximum laser power
    laser_fluc_data_corrected[:,ii]=laser_fluc_data[:,ii]+difference[ii] #calibrate the laser power references with the crystal 
    transmission_data_corrected[:,ii]=data[ii,:,3]+difference[ii] #calibrate the transmitted signals with the crystal
    ref_array_max=np.amax(laser_fluc_of_ref[:,ii]) #find out the maximum laser power of each laser polarisation (witouth the crystal)
    ref_difference[ii]=laser_power_max-ref_array_max #calculate the difference of laser maximal of each laser polarisation with the maximum laser power
    laser_fluc_of_ref_corrected[:,ii]=laser_fluc_of_ref[:,ii]+ref_difference[ii] #calibrate the laser power references without the crystal 
    transmission_ref_data_corrected[:,ii]=ref_data[ii,:,3]+ref_difference[ii] #calibrate the transmitted signals without the crystal
    absorption_corrected[:,ii]=np.log(transmission_ref_data_corrected[:,ii]/transmission_data_corrected[:,ii]) #calculate OD based on the calibrated signals

#try to fit the absorption
#for jj in range(num_files):
    #jj=0
    #absorption_max[jj]=np.amax(absorption[:,jj])
    #location_1 = np.where(absorption[:,jj] == absorption_max[jj])
    #location_absorption_max[jj]=location_1[0]
    #OD_peak_index=signal.find_peaks(absorption[:,jj],distance=16000)
    #OD_peak_index=OD_peak_index[0]
    #absorption_valley=absorption[:,jj]*(-1)
    #OD_valley_index=signal.find_peaks(absorption_valley,distance=16000)
    #OD_valley_index=OD_valley_index[0]
    #print(OD_peak_index)
    #print(OD_valley_index)
    #test=1

#plotting all figures, but we can set an option to show which figure at the begining 
#plt.figure()
#plot calculated OD based on the raw data
for index in range(num_files):
    plt.plot(time_scale, absorption[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('OD')
    #plt.title('Measured OD at 1550.267 nm (based on raw data)')
    plt.title('Measured OD at 605.977 nm (based on raw data)')
    plt.legend()
    
plt.show()

#plt.figure(2)
for index in range(num_files):
    plt.plot(time_scale, laser_fluc_data[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity (V)')
    plt.title('Laser power fluctuation before the cryostat (with crystal)')
    plt.legend()

plt.show()

for index in range(num_files):
    plt.plot(time_scale, laser_fluc_data_corrected[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity (V)')
    plt.title('Calibrated laser power fluctuation before the cryostat (with crystal)')
    plt.legend()

plt.show()

for index in range(num_files):
    plt.plot(time_scale, transmission_data[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity (V)')
    plt.title('Transmitted signal (with crystal)')
    plt.legend()

plt.show()

for index in range(num_files):
    plt.plot(time_scale, transmission_data_corrected[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity (V)')
    plt.title('Calibrated transmitted signal (with crystal)')
    plt.legend()

plt.show()

for index in range(num_files):
    plt.plot(time_scale, laser_fluc_of_ref[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity (V)')
    plt.title('Laser power fluctuation before the cryostat (without crystal)')
    plt.legend()
    
plt.show()

for index in range(num_files):
    plt.plot(time_scale, laser_fluc_of_ref_corrected[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity (V)')
    plt.title('Calibrated laser power fluctuation before the cryostat (without crystal)')
    plt.legend()
    
plt.show()

for index in range(num_files):
    plt.plot(time_scale, transmission_ref_data[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity (V)')
    plt.title('Transmitted reference signal (without crystal)')
    plt.legend()

plt.show()

for index in range(num_files):
    plt.plot(time_scale, transmission_ref_data_corrected[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('Intensity (V)')
    plt.title('Calibrated transmitted reference signal (without crystal)')
    plt.legend()
    
plt.show()

for index in range(num_files):
    plt.plot(time_scale, absorption_corrected[:,index],label="{}".format(angle_of_half_waveplate[index]))
    plt.xlabel('Time (s)')
    plt.ylabel('OD')
    #plt.title('Measured OD at 1550.267 nm (based on calibrated data)')
    plt.title('Measured OD at 605.977 nm (based on calibrated data)')
    plt.legend()
    
plt.show()