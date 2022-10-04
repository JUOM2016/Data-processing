# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 14:33:38 2022

@author: Wei Jiang

The program is used to deal with the data of spectral hole burning experiments;

A excel file including the parameters used for the generation of the pulse sequence
from a HDAWG is necessary. If you want to know the layout of the excel file, please 
contact Wei.
"""

import os
import numpy as np
import pandas as pd
from natsort import natsorted
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys

# Directory and folder for data
dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU\\20220622_Pr_YSO_SHB_pit'
folder = '20220622_burnback'

path = dir + '\\' + folder + '\\'
file_list = os.listdir(path)

# Listing all .csv files but not all data fies will be used in some cases
list_csv=natsorted([i for i in file_list if i.endswith('.CSV')])

# Finding the excel file to know experimental conditions and variables
list_xlsx=natsorted([i for i in file_list if i.endswith('.xlsx')])
if not list_xlsx:
        sys.exit('Excel file does not exist or must be of format ".xlsx"')
xlsx = pd.ExcelFile(path + list_xlsx[0])
print(list_xlsx[0])

# Finding out references
# ***IMPORTANT***
# Flag=0 --> Burning data; 
# Flag=1 --> Reference data; (without the crystal or laser polarisation along b-axis)
# Flag=2 --> Data when switching OFF burning pulses
read_xlsx= pd.read_excel(xlsx, sheet_name='Sheet1')
read_flag= pd.read_excel(xlsx, sheet_name='Sheet1', usecols=['Flag'])
flagNum = np.reshape(read_flag.to_numpy(), len(read_flag))
xlsx_size=read_xlsx.shape

# Setting some conditions when doing the measurements
#variable='Central frequency of  burnback pulse (MHz)'
#variable='Amplitude of second chirp sine wave (V)'
variable='Amplitude of burnback pulse (V)'
index_of_variable=read_xlsx.columns.get_loc(variable)
index_of_FileName=read_xlsx.columns.get_loc('File name')

# Listing all data files when switching on the burning pulse
find_Burning=np.where(flagNum == 0) # flagNum is 0 when switching on burning 
Burning_index=np.transpose(np.array(find_Burning))
Burning_index_len=len(Burning_index)
Burning_csv_list=np.empty([Burning_index_len,xlsx_size[1]],dtype='U25')
for index in range(Burning_index_len):
    Burning_csv_list0=read_xlsx.loc[int(Burning_index[index])]
    Burning_csv_list0=Burning_csv_list0.to_frame()
    Burning_csv_list0=Burning_csv_list0.T
    Burning_csv_list1=Burning_csv_list0.to_numpy()
    for ii in range(len(Burning_csv_list1.T)-1):
        Burning_csv_list[index,ii]=Burning_csv_list1[0,ii]

# Listing all reference files
find_references=np.where(flagNum == 1) #flagNum is 1, the data are the references(without crystal or along b(or D1) axis) 
ref_index=np.transpose(np.array(find_references))
ref_index_len=len(ref_index)
ref_csv_list=np.empty([ref_index_len,xlsx_size[1]],dtype='U25')
for index in range(ref_index_len):
    ref_csv_list0=read_xlsx.loc[int(ref_index[index])]
    ref_csv_list0=ref_csv_list0.to_frame()
    ref_csv_list0=ref_csv_list0.T
    ref_csv_list1=ref_csv_list0.to_numpy()
    for ii in range(len(ref_csv_list1.T)-1):
        ref_csv_list[index,ii]=ref_csv_list1[0,ii]

# Reading a random .csv file to achieve the time scale
read_example=pd.read_csv(os.path.join(path,Burning_csv_list[0,0] +'.'+'csv'))
read_example=read_example.to_numpy()
row_of_data, column_of_data=np.shape(read_example)
time_scale_example=read_example[:,0]
time_scale_len=len(time_scale_example)

# Initialising arrays 
Burning_csv=np.zeros([Burning_index_len,xlsx_size[1]],dtype=np.int64)
Burning_data=np.empty([Burning_index_len,time_scale_len,column_of_data])
Burning_csv_variable_num=np.empty([Burning_index_len,1])
Burning_data_corrected=np.empty([Burning_index_len,time_scale_len,1])
ref_data=np.empty([ref_index_len,time_scale_len,column_of_data])
ref_data_corrected=np.empty([ref_index_len,time_scale_len,1])
noBurning_data=np.empty([ref_index_len,time_scale_len,column_of_data])
noBurning_data_corrected=np.empty([ref_index_len,time_scale_len,1])
absorption_Burning=np.empty([Burning_index_len,time_scale_len,1])
absorption_Burning_corrected=np.empty([Burning_index_len,time_scale_len,1])
absorption_noBurning=np.empty([Burning_index_len,time_scale_len,1])
absorption_noBurning_corrected=np.empty([Burning_index_len,time_scale_len,1])
time_scale=np.empty([Burning_index_len,time_scale_len,1])
frequency_scale=np.empty([Burning_index_len,time_scale_len,1])

# Identifing whether there are data when switching off the burning pulse (flagNum is 2 when switching off the burning pulse)
read_flag_1=read_flag.to_numpy()
read_flag_1=str(read_flag_1[:,:])

if '2' not in read_flag_1:    
    print('No data when switching off burning pulse')
    # Finding out the different experimental conditions (based on variable set above) and recording them
    column_of_ref_variable_0=ref_csv_list[:,index_of_variable]
    column_of_ref_variable=np.empty([ref_index_len,1])
    for index in range(ref_index_len):
        column_of_ref_variable[index,0]=float(column_of_ref_variable_0[index])
    
    for index in range(Burning_index_len):
        # Find the data when switching on the burning pulse
        Burning_csv=read_xlsx.loc[Burning_index[index]]
        Burning_csv_name=pd.DataFrame(Burning_csv, columns= ['File name'])
        Burning_csv_name_1=Burning_csv_name.to_numpy()
        Burning_csv_name=str(Burning_csv_name_1[0,0])
        Burning_csv_variable=pd.DataFrame(Burning_csv, columns= [variable])
        Burning_csv_variable_1=Burning_csv_variable.to_numpy()
        Burning_csv_variable=Burning_csv_variable_1[0,0]
        Burning_csv_variable_num[index,0]=Burning_csv_variable_1[0,0]
        read_Burning_data=pd.read_csv(os.path.join(path,Burning_csv_name +'.'+'csv'))
        Burning_data[index,:,:]=read_Burning_data.to_numpy()
        Burning_data_corrected[index,:,0]=Burning_data[index,:,2]-min(Burning_data[index,:,2])+0.0000001
        time_scale[index,:,0]=Burning_data[index,:,0]
        # find the corresponding reference data
        loc_ref=np.where(column_of_ref_variable == Burning_csv_variable)
        corresponding_ref_name=ref_csv_list[loc_ref[0],index_of_FileName]
        read_ref_data=pd.read_csv(os.path.join(path,corresponding_ref_name[0] +'.'+'csv'))
        ref_data[index,:,:]=read_ref_data.to_numpy()
        ref_data_corrected[index,:,0]=ref_data[index,:,2]-min(ref_data[index,:,2])+0.0000001
        
        absorption_Burning[index,:,0]=np.log(ref_data[index,:,2]/Burning_data[index,:,2])
        absorption_Burning_corrected[index,:,0]=np.log(ref_data_corrected[index,:,0]/Burning_data_corrected[index,:,0])
    
        reading_pulse_duation=pd.DataFrame(Burning_csv, columns= ['Pulse width of second chirp sine wave (ms)'])
        reading_pulse_freq_detuning=pd.DataFrame(Burning_csv, columns= ['Frequency detuning of second chirp sine wave (MHz)'])
        reading_pulse_duation=reading_pulse_duation.to_numpy()
        reading_pulse_freq_detuning=reading_pulse_freq_detuning.to_numpy()
        frequency_scale[index,:,0]=time_scale[index,:,0]/(reading_pulse_duation*1e-3)*reading_pulse_freq_detuning
    fig, ax=plt.subplots()
    for index in range(Burning_index_len-1):
        ax.plot(frequency_scale[index,:,0],absorption_Burning_corrected[index,:,0],label="{}".format(Burning_csv_variable_num[index,0]))
        #ax.plot(time_scale,absorption_Burning_corrected[index,:,0])
    #ax.set_xlabel('Time(s)')
    ax.set_xlabel('Frequency detuning (MHz)')
    ax.set_ylabel('OD')
    ax.legend(loc=1,title='Amplitude of reading-out pulse',fontsize='x-small',title_fontsize='x-small')
    plt.show()
    
if '2' in read_flag_1:
    print('There are data when switching off burning pulse')
    find_noBurning=np.where(flagNum == 2) # flagNum is 0 when switching OFF burning 
    noBurning_index=np.transpose(np.array(find_noBurning))
    noBurning_index_len=len(noBurning_index)
    noBurning_csv_list=np.empty([noBurning_index_len,xlsx_size[1]],dtype='U25')
    for index in range(noBurning_index_len):
        noBurning_csv_list0=read_xlsx.loc[int(noBurning_index[index])]
        noBurning_csv_list0=noBurning_csv_list0.to_frame()
        noBurning_csv_list0=noBurning_csv_list0.T
        noBurning_csv_list1=noBurning_csv_list0.to_numpy()
        for ii in range(len(noBurning_csv_list1.T)-1):
            noBurning_csv_list[index,ii]=noBurning_csv_list1[0,ii]
    
    column_of_ref_variable_0=ref_csv_list[:,index_of_variable]
    column_of_ref_variable=np.empty([ref_index_len,1])
    for index in range(ref_index_len):
        column_of_ref_variable[index,0]=float(column_of_ref_variable_0[index])
        
    column_of_noBurning_variable_0=ref_csv_list[:,index_of_variable]
    column_of_noBurning_variable=np.empty([noBurning_index_len,1])
    for index in range(noBurning_index_len):
        column_of_noBurning_variable[index,0]=float(column_of_noBurning_variable_0[index])
    
    for index in range(Burning_index_len):
        # find the data when switching on the burning pulse
        Burning_csv=read_xlsx.loc[Burning_index[index]]
        Burning_csv_name=pd.DataFrame(Burning_csv, columns= ['File name'])
        Burning_csv_name_1=Burning_csv_name.to_numpy()
        Burning_csv_name=str(Burning_csv_name_1[0,0])
        Burning_csv_variable=pd.DataFrame(Burning_csv, columns= [variable])
        Burning_csv_variable_1=Burning_csv_variable.to_numpy()
        Burning_csv_variable=Burning_csv_variable_1[0,0]
        Burning_csv_variable_num[index,0]=Burning_csv_variable_1[0,0]
        read_Burning_data=pd.read_csv(os.path.join(path,Burning_csv_name +'.'+'csv'))
        Burning_data[index,:,:]=read_Burning_data.to_numpy()
        Burning_data_corrected[index,:,0]=Burning_data[index,:,2]-min(Burning_data[index,:,2])+0.0000001
        time_scale[index,:,0]=Burning_data[index,:,0]
        # find the corresponding reference data
        loc_ref=np.where(column_of_ref_variable == Burning_csv_variable)
        corresponding_ref_name=ref_csv_list[loc_ref[0],index_of_FileName]
        read_ref_data=pd.read_csv(os.path.join(path,corresponding_ref_name[0] +'.'+'csv'))
        ref_data[index,:,:]=read_ref_data.to_numpy()
        ref_data_corrected[index,:,0]=ref_data[index,:,2]-min(ref_data[index,:,2])+0.0000001
        # find the corresponding noBurning data
        loc_noBurning=np.where(column_of_noBurning_variable == Burning_csv_variable)
        corresponding_noBurning_name=ref_csv_list[loc_noBurning[0],index_of_FileName]
        read_noBurning_data=pd.read_csv(os.path.join(path,corresponding_noBurning_name[0] +'.'+'csv'))
        noBurning_data[index,:,:]=read_noBurning_data.to_numpy()
        noBurning_data_corrected[index,:,0]=noBurning_data[index,:,2]-min(noBurning_data[index,:,2])+0.0000001
        
        absorption_Burning[index,:,0]=np.log(ref_data[index,:,2]/Burning_data[index,:,2])
        absorption_Burning_corrected[index,:,0]=np.log(ref_data_corrected[index,:,0]/Burning_data_corrected[index,:,0])
        
        absorption_noBurning[index,:,0]=np.log(ref_data[index,:,2]/noBurning_data[index,:,2])
        absorption_noBurning_corrected[index,:,0]=np.log(ref_data_corrected[index,:,0]/noBurning_data_corrected[index,:,0])
        
        #reading_pulse_duation=pd.DataFrame(Burning_csv, columns= ['Pulse duration of   read-out pulse (ms)'])
        #reading_pulse_freq_detuning=pd.DataFrame(Burning_csv, columns= ['Frequency detuning of  read-out pulse (MHz)'])
        reading_pulse_duation=pd.DataFrame(Burning_csv, columns= ['Pulse duration of   read-out pulse (ms)'])
        reading_pulse_freq_detuning=pd.DataFrame(Burning_csv, columns= ['Read-out pulse frequency sweeping (MHz)'])
        reading_pulse_duation=reading_pulse_duation.to_numpy()
        reading_pulse_freq_detuning=reading_pulse_freq_detuning.to_numpy()
        frequency_scale[index,:,0]=time_scale[index,:,0]/(reading_pulse_duation*1e-3)*reading_pulse_freq_detuning
        
    for index in range(Burning_index_len):
        fig, ax=plt.subplots()    
        ax.plot(frequency_scale[index,:,0],absorption_Burning_corrected[index,:,0],label="{}".format(Burning_csv_variable_num[index,0]))
        ax.plot(frequency_scale[index,:,0],absorption_noBurning[index,:,0])
        #ax.plot(time_scale[index,:,0],absorption_Burning_corrected[index,:,0])
        #ax.set_xlabel('Time(s)')
        ax.set_xlabel('Frequency detuning (MHz)')
        ax.set_ylabel('OD')
        ax.legend(loc=1,title='Amplitude of reading-out pulse',fontsize='x-small',title_fontsize='x-small')
    plt.show()
