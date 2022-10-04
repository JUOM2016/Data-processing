# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 12:26:41 2022

@author: Wei Jiang
"""
import os
import numpy as np
import pandas as pd
from natsort import natsorted
import matplotlib.pyplot as plt
import sys

# Directory and folder for data
dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU'
folder = '20220727_Pr_YSO_SHB'

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

#****************************************************
#*******Need to change the variable everytime********
# Setting some conditions when doing the measurements
#variable='Central frequency of  burnback pulse (MHz)'
#variable='Amplitude of second chirp sine wave (V)'
variable='Pulse duration of burning pulse (ms)'
index_of_variable=read_xlsx.columns.get_loc(variable)
index_of_FileName=read_xlsx.columns.get_loc('File name')

# Indentify how many kinds of data have been measured and need to cope with
flag=np.array([])
index_flag=1
repeat_num=0
flag=flagNum[0]
while index_flag<len(flagNum):
    flag_1=str(flag)
    if "{}".format(flagNum[index_flag]) in flag_1:
        repeat_num=repeat_num+1
    elif "{}".format(flagNum[index_flag]) not in flag_1:
        flag=np.append(flag, 1000)
        flag[index_flag-repeat_num]=flagNum[index_flag]
    index_flag=index_flag+1

# Classifing and listing measured files
for index in range(len(flag)):
    if flag[index]==0:
        # Listing all data files when switching on all pulses (burning, burning-back, and cleaning pulses)
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
        absorption_Burning=np.empty([1,time_scale_len,Burning_index_len])
        absorption_Burning_corrected=np.empty([1,time_scale_len,Burning_index_len])
        
    elif flag[index]==1:
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
        read_example=pd.read_csv(os.path.join(path,ref_csv_list[0,0] +'.'+'csv'))
        read_example=read_example.to_numpy()
        row_of_data, column_of_data=np.shape(read_example)
        time_scale_example=read_example[:,0]
        time_scale_len=len(time_scale_example)
        # Initialising arrays 
        ref_data=np.empty([ref_index_len,time_scale_len,3]) #column_of_data
        ref_data_corrected=np.empty([ref_index_len,time_scale_len,1])
        time_scale=np.empty([ref_index_len,time_scale_len,1])
        frequency_scale=np.empty([ref_index_len,time_scale_len,1])
        
    elif flag[index]==2:
        # Listing all data files when switching off burning, burning-back, and cleaning pulses, but switching on the read pulse
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
        # Reading a random .csv file to achieve the time scale
        read_example=pd.read_csv(os.path.join(path,noBurning_csv_list[0,0] +'.'+'csv'))
        read_example=read_example.to_numpy()
        row_of_data, column_of_data=np.shape(read_example)
        time_scale_example=read_example[:,0]
        time_scale_len=len(time_scale_example)
        # Initialising arrays 
        noBurning_data=np.empty([noBurning_index_len,time_scale_len,column_of_data])
        noBurning_csv_variable_num=np.empty([noBurning_index_len,1])
        noBurning_data_corrected=np.empty([noBurning_index_len,time_scale_len,1])
        absorption_noBurning=np.empty([1,time_scale_len,noBurning_index_len])
        absorption_noBurning_corrected=np.empty([1,time_scale_len,noBurning_index_len])
        
    elif flag[index]==3:
        # Listing files when ONLY switching on burning + burning-back pulses)
        find_burn_and_burn_back=np.where(flagNum == 3) #flagNum is 1, the data are the references(without crystal or along b(or D1) axis) 
        burn_and_burn_back_index=np.transpose(np.array(find_burn_and_burn_back))
        burn_and_burn_back_index_len=len(burn_and_burn_back_index)
        burn_and_burn_back_csv_list=np.empty([burn_and_burn_back_index_len,xlsx_size[1]],dtype='U25')
        for index in range(burn_and_burn_back_index_len):
            burn_and_burn_back_csv_list0=read_xlsx.loc[int(burn_and_burn_back_index[index])]
            burn_and_burn_back_csv_list0=burn_and_burn_back_csv_list0.to_frame()
            burn_and_burn_back_csv_list0=burn_and_burn_back_csv_list0.T
            burn_and_burn_back_csv_list1=burn_and_burn_back_csv_list0.to_numpy()
            for ii in range(len(burn_and_burn_back_csv_list1.T)-1):
                burn_and_burn_back_csv_list[index,ii]=burn_and_burn_back_csv_list1[0,ii]
        # Reading a random .csv file to achieve the time scale
        read_example=pd.read_csv(os.path.join(path,burn_and_burn_back_csv_list[0,0] +'.'+'csv'))
        read_example=read_example.to_numpy()
        row_of_data, column_of_data=np.shape(read_example)
        time_scale_example=read_example[:,0]
        time_scale_len=len(time_scale_example)
        # Initialising arrays 
        burn_and_burn_back_data=np.empty([burn_and_burn_back_index_len,time_scale_len,column_of_data])
        burn_and_burn_back_data_corrected=np.empty([burn_and_burn_back_index_len,time_scale_len,1])
        burn_and_burn_back_csv_variable_num=np.empty([burn_and_burn_back_index_len,1])
        absorption_burn_and_burn_back=np.empty([1,time_scale_len,burn_and_burn_back_index_len])
        absorption_burn_and_burn_back_corrected=np.empty([1,time_scale_len,burn_and_burn_back_index_len])
        
    elif flag[index]==4:
        # Listing files of spectral pit (ONLY switching on burning pulses)
        find_pit=np.where(flagNum == 4) #flagNum is 1, the data are the references(without crystal or along b(or D1) axis) 
        pit_index=np.transpose(np.array(find_pit))
        pit_index_len=len(pit_index)
        pit_csv_list=np.empty([pit_index_len,xlsx_size[1]],dtype='U25')
        for index in range(pit_index_len):
            pit_csv_list0=read_xlsx.loc[int(pit_index[index])]
            pit_csv_list0=pit_csv_list0.to_frame()
            pit_csv_list0=pit_csv_list0.T
            pit_csv_list1=pit_csv_list0.to_numpy()
            for ii in range(len(pit_csv_list1.T)-1):
                pit_csv_list[index,ii]=pit_csv_list1[0,ii]
        # Reading a random .csv file to achieve the time scale
        read_example=pd.read_csv(os.path.join(path,pit_csv_list[0,0] +'.'+'csv'))
        read_example=read_example.to_numpy()
        row_of_data, column_of_data=np.shape(read_example)
        time_scale_example=read_example[:,0]
        time_scale_len=len(time_scale_example)
        # Initialising arrays
        pit_data=np.zeros([pit_index_len,time_scale_len,column_of_data])
        pit_data_corrected=np.empty([pit_index_len,time_scale_len,1])
        pit_csv_variable_num=np.empty([pit_index_len,1])
        absorption_pit=np.empty([1,time_scale_len,pit_index_len])
        absorption_pit_corrected=np.empty([1,time_scale_len,pit_index_len])

if '1' not in flag_1:# No reference data
    print('There is no reference data, so plese check the raw data!')
elif '1' in flag_1:
    # Finding out the different experimental conditions (based on variable set above) and recording them
    column_of_ref_variable_0=ref_csv_list[:,index_of_variable]
    column_of_ref_variable=np.empty([ref_index_len,1])
    for index in range(ref_index_len):
        column_of_ref_variable[index,0]=float(column_of_ref_variable_0[index])
        
    if ref_index_len == 1: # Sometime only to have one reference for all measurements, so this is only one reference 
        for index in range(len(flag)):
            # find the corresponding reference data
            read_ref_data=pd.read_csv(os.path.join(path,ref_csv_list[0,0] +'.'+'csv'))
            ref_data[index,:,:]=read_ref_data.to_numpy()
            ref_data_corrected[index,:,0]=ref_data[index,:,2]-min(ref_data[index,:,2])+0.0000001
            if flag[index]==0:
                for index in range(Burning_index_len):
                    # Find the data when switching on all pulses (burning, burning-back, and cleaning pulses)
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
                    
                    absorption_Burning[0,:,index]=np.log(ref_data[index,:,2]/Burning_data[index,:,2])
                    absorption_Burning_corrected[0,:,index]=np.log(ref_data_corrected[index,:,0]/Burning_data_corrected[index,:,0])
            elif flag[index]==2:
                for index in range(noBurning_index_len):
                    #
                    noBurning_csv=read_xlsx.loc[noBurning_index[index]]
                    noBurning_csv_name=pd.DataFrame(noBurning_csv, columns= ['File name'])
                    noBurning_csv_name_1=noBurning_csv_name.to_numpy()
                    noBurning_csv_name=str(noBurning_csv_name_1[0,0])
                    noBurning_csv_variable=pd.DataFrame(noBurning_csv, columns= [variable])
                    noBurning_csv_variable_1=noBurning_csv_variable.to_numpy()
                    noBurning_csv_variable=noBurning_csv_variable_1[0,0]
                    noBurning_csv_variable_num[index,0]=noBurning_csv_variable_1[0,0]
                    read_noBurning_data=pd.read_csv(os.path.join(path,noBurning_csv_name +'.'+'csv'))
                    noBurning_data[index,:,:]=read_noBurning_data.to_numpy()
                    noBurning_data_corrected[index,:,0]=noBurning_data[index,:,2]-min(noBurning_data[index,:,2])+0.0000001
                    time_scale[index,:,0]=noBurning_data[index,:,0]
                    
                    absorption_noBurning[0,:,index]=np.log(ref_data[index,:,2]/noBurning_data[index,:,2])
                    absorption_noBurning_corrected[0,:,index]=np.log(ref_data_corrected[index,:,0]/noBurning_data_corrected[index,:,0])
                    
            elif flag[index]==3:
                for index in range(burn_and_burn_back_index_len):
                    # 
                    burn_and_burn_back_csv=read_xlsx.loc[burn_and_burn_back_index[index]]
                    burn_and_burn_back_csv_name=pd.DataFrame(burn_and_burn_back_csv, columns= ['File name'])
                    burn_and_burn_back_csv_name_1=burn_and_burn_back_csv_name.to_numpy()
                    burn_and_burn_back_csv_name=str(burn_and_burn_back_csv_name_1[0,0])
                    burn_and_burn_back_csv_variable=pd.DataFrame(burn_and_burn_back_csv, columns= [variable])
                    burn_and_burn_back_csv_variable_1=burn_and_burn_back_csv_variable.to_numpy()
                    burn_and_burn_back_csv_variable=burn_and_burn_back_csv_variable_1[0,0]
                    burn_and_burn_back_csv_variable_num[index,0]=burn_and_burn_back_csv_variable_1[0,0]
                    read_burn_and_burn_back_data=pd.read_csv(os.path.join(path,burn_and_burn_back_csv_name +'.'+'csv'))
                    burn_and_burn_back_data[index,:,:]=read_burn_and_burn_back_data.to_numpy()
                    burn_and_burn_back_data_corrected[index,:,0]=burn_and_burn_back_data[index,:,2]-min(burn_and_burn_back_data[index,:,2])+0.0000001
                    #time_scale[index,:,0]=burn_and_burn_back_data[index,:,0]
                    # find the only reference data
                    read_ref_data=pd.read_csv(os.path.join(path,ref_csv_list[0,0] +'.'+'csv'))
                    ref_data[index,:,:]=read_ref_data.to_numpy()
                    ref_data_corrected[index,:,0]=ref_data[index,:,2]-min(ref_data[index,:,2])+0.0000001
                    
                    absorption_burn_and_burn_back[0,:,index]=np.log(ref_data[0,:,2]/burn_and_burn_back_data[index,:,2])
                    absorption_burn_and_burn_back_corrected[0,:,index]=np.log(ref_data_corrected[0,:,0]/burn_and_burn_back_data_corrected[index,:,0])
            elif flag[index]==4:
                for index in range(pit_index_len):
                    # 
                    pit_csv=read_xlsx.loc[pit_index[index]]
                    pit_csv_name=pd.DataFrame(pit_csv, columns= ['File name'])
                    pit_csv_name_1=pit_csv_name.to_numpy()
                    pit_csv_name=str(pit_csv_name_1[0,0])
                    pit_csv_variable=pd.DataFrame(pit_csv, columns= [variable])
                    pit_csv_variable_1=pit_csv_variable.to_numpy()
                    pit_csv_variable=pit_csv_variable_1[0,0]
                    pit_csv_variable_num[index,0]=pit_csv_variable_1[0,0]
                    read_pit_data=pd.read_csv(os.path.join(path,pit_csv_name +'.'+'csv'))
                    pit_data[index,:,:]=read_pit_data.to_numpy()
                    pit_data_corrected[index,:,0]=pit_data[index,:,2]-min(pit_data[index,:,2])+0.0000001
                    #time_scale[index,:,0]=pit_data[index,:,0]
                    # find the only reference data
                    read_ref_data=pd.read_csv(os.path.join(path,ref_csv_list[0,0] +'.'+'csv'))
                    ref_data[index,:,:]=read_ref_data.to_numpy()
                    ref_data_corrected[index,:,0]=ref_data[index,:,2]-min(ref_data[index,:,2])+0.0000001
                    
                    absorption_pit[0,:,index]=np.log(ref_data[0,:,2]/pit_data[index,:,2])
                    absorption_pit_corrected[0,:,index]=np.log(ref_data_corrected[0,:,0]/pit_data_corrected[index,:,0])
                    
    elif ref_index_len != 1: # More than one reference
        for index in range(len(flag)):
            if flag[index]==0:
                for index in range(Burning_index_len):
                    # find the data when switching on all pulses (burning, burning-back, and cleaning pulses)
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
                    
                    absorption_Burning[0,:,index]=np.log(ref_data[index,:,2]/Burning_data[index,:,2])
                    absorption_Burning_corrected[0,:,index]=np.log(ref_data_corrected[index,:,0]/Burning_data_corrected[index,:,0])
                    
                    reading_pulse_duation=pd.DataFrame(Burning_csv, columns= ['Pulse duration of   read-out pulse (ms)'])
                    reading_pulse_freq_sweeping=pd.DataFrame(Burning_csv, columns= ['Read-out pulse frequency sweeping (MHz)'])
                    reading_pulse_duation=reading_pulse_duation.to_numpy()
                    reading_pulse_freq_sweeping=reading_pulse_freq_sweeping.to_numpy()
                    frequency_scale[index,:,0]=time_scale[index,:,0]/(reading_pulse_duation*1e-3)*reading_pulse_freq_sweeping
            elif flag[index]==2:
                for index in range(noBurning_index_len):
                    #
                    noBurning_csv=read_xlsx.loc[noBurning_index[index]]
                    noBurning_csv_name=pd.DataFrame(noBurning_csv, columns= ['File name'])
                    noBurning_csv_name_1=noBurning_csv_name.to_numpy()
                    noBurning_csv_name=str(noBurning_csv_name_1[0,0])
                    noBurning_csv_variable=pd.DataFrame(noBurning_csv, columns= [variable])
                    noBurning_csv_variable_1=noBurning_csv_variable.to_numpy()
                    noBurning_csv_variable=noBurning_csv_variable_1[0,0]
                    noBurning_csv_variable_num[index,0]=noBurning_csv_variable_1[0,0]
                    read_noBurning_data=pd.read_csv(os.path.join(path,noBurning_csv_name +'.'+'csv'))
                    noBurning_data[index,:,:]=read_noBurning_data.to_numpy()
                    noBurning_data_corrected[index,:,0]=noBurning_data[index,:,2]-min(noBurning_data[index,:,2])+0.0000001
                    time_scale[index,:,0]=noBurning_data[index,:,0]
                    # find the corresponding reference data
                    loc_ref=np.where(column_of_ref_variable == noBurning_csv_variable)
                    corresponding_ref_name=ref_csv_list[loc_ref[0],index_of_FileName]
                    read_ref_data=pd.read_csv(os.path.join(path,corresponding_ref_name[0] +'.'+'csv'))
                    ref_data[index,:,:]=read_ref_data.to_numpy()
                    ref_data_corrected[index,:,0]=ref_data[index,:,2]-min(ref_data[index,:,2])+0.0000001
                    
                    absorption_noBurning[0,:,index]=np.log(ref_data[index,:,2]/noBurning_data[index,:,2])
                    absorption_noBurning_corrected[0,:,index]=np.log(ref_data_corrected[index,:,0]/noBurning_data_corrected[index,:,0])
                    
                    reading_pulse_duation=pd.DataFrame(noBurning_csv, columns= ['Pulse duration of   read-out pulse (ms)'])
                    reading_pulse_freq_sweeping=pd.DataFrame(noBurning_csv, columns= ['Read-out pulse frequency sweeping (MHz)'])
                    reading_pulse_duation=reading_pulse_duation.to_numpy()
                    reading_pulse_freq_sweeping=reading_pulse_freq_sweeping.to_numpy()
                    frequency_scale[index,:,0]=time_scale[index,:,0]/(reading_pulse_duation*1e-3)*reading_pulse_freq_sweeping
            elif flag[index]==3:
                for index in range(burn_and_burn_back_index_len):
                    burn_and_burn_back_csv=read_xlsx.loc[burn_and_burn_back_index[index]]
                    burn_and_burn_back_csv_name=pd.DataFrame(burn_and_burn_back_csv, columns= ['File name'])
                    burn_and_burn_back_csv_name_1=burn_and_burn_back_csv_name.to_numpy()
                    burn_and_burn_back_csv_name=str(burn_and_burn_back_csv_name_1[0,0])
                    burn_and_burn_back_csv_variable=pd.DataFrame(burn_and_burn_back_csv, columns= [variable])
                    burn_and_burn_back_csv_variable_1=burn_and_burn_back_csv_variable.to_numpy()
                    burn_and_burn_back_csv_variable=burn_and_burn_back_csv_variable_1[0,0]
                    burn_and_burn_back_csv_variable_num[index,0]=burn_and_burn_back_csv_variable_1[0,0]
                    read_burn_and_burn_back_data=pd.read_csv(os.path.join(path,burn_and_burn_back_csv_name +'.'+'csv'))
                    burn_and_burn_back_data[index,:,:]=read_burn_and_burn_back_data.to_numpy()
                    burn_and_burn_back_data_corrected[index,:,0]=burn_and_burn_back_data[index,:,2]-min(burn_and_burn_back_data[index,:,2])+0.0000001
                    time_scale[index,:,0]=burn_and_burn_back_data[index,:,0]
                    # find the corresponding reference data
                    loc_ref=np.where(column_of_ref_variable == burn_and_burn_back_csv_variable)
                    corresponding_ref_name=ref_csv_list[loc_ref[0],index_of_FileName]
                    read_ref_data=pd.read_csv(os.path.join(path,corresponding_ref_name[0] +'.'+'csv'))
                    ref_data[index,:,:]=read_ref_data.to_numpy()
                    ref_data_corrected[index,:,0]=ref_data[index,:,2]-min(ref_data[index,:,2])+0.0000001
                             
                    absorption_burn_and_burn_back[0,:,index]=np.log(ref_data[index,:,2]/burn_and_burn_back_data[index,:,2])
                    absorption_burn_and_burn_back_corrected[0,:,index]=np.log(ref_data_corrected[index,:,0]/burn_and_burn_back_data_corrected[index,:,0])
                    
                    reading_pulse_duation=pd.DataFrame(burn_and_burn_back_csv, columns= ['Pulse duration of   read-out pulse (ms)'])
                    reading_pulse_freq_sweeping=pd.DataFrame(burn_and_burn_back_csv, columns= ['Read-out pulse frequency sweeping (MHz)'])
                    reading_pulse_duation=reading_pulse_duation.to_numpy()
                    reading_pulse_freq_sweeping=reading_pulse_freq_sweeping.to_numpy()
                    frequency_scale[index,:,0]=time_scale[index,:,0]/(reading_pulse_duation*1e-3)*reading_pulse_freq_sweeping
            elif flag[index]==4:
                for index in range(pit_index_len):
                    pit_csv=read_xlsx.loc[pit_index[index]]
                    pit_csv_name=pd.DataFrame(pit_csv, columns= ['File name'])
                    pit_csv_name_1=pit_csv_name.to_numpy()
                    pit_csv_name=str(pit_csv_name_1[0,0])
                    pit_csv_variable=pd.DataFrame(pit_csv, columns= [variable])
                    pit_csv_variable_1=pit_csv_variable.to_numpy()
                    pit_csv_variable=pit_csv_variable_1[0,0]
                    pit_csv_variable_num[index,0]=pit_csv_variable_1[0,0]
                    read_pit_data=pd.read_csv(os.path.join(path,pit_csv_name +'.'+'csv'))
                    pit_data_0=read_pit_data.to_numpy()
                    pit_data[index,:,:]=pit_data_0
                    pit_data_corrected[index,:,0]=pit_data[index,:,2]-min(pit_data[index,:,2])+0.0000001
                    time_scale[index,:,0]=pit_data[index,:,0]
                    # find the corresponding reference data
                    loc_ref=np.where(column_of_ref_variable == pit_csv_variable)
                    corresponding_ref_name=ref_csv_list[loc_ref[0],index_of_FileName]
                    read_ref_data=pd.read_csv(os.path.join(path,corresponding_ref_name[0] +'.'+'csv'))
                    ref_data[index,:,:]=read_ref_data.to_numpy()
                    ref_data_corrected[index,:,0]=ref_data[index,:,2]-min(ref_data[index,:,2])+0.0000001
                             
                    absorption_pit[0,:,index]=np.log(ref_data[index,:,2]/pit_data[index,:,2])
                    absorption_pit_corrected[0,:,index]=np.log(ref_data_corrected[index,:,0]/pit_data_corrected[index,:,0])
                    
                    reading_pulse_duation=pd.DataFrame(pit_csv, columns= ['Pulse duration of   read-out pulse (ms)'])
                    reading_pulse_freq_sweeping=pd.DataFrame(pit_csv, columns= ['Read-out pulse frequency sweeping (MHz)'])
                    reading_pulse_duation=reading_pulse_duation.to_numpy()
                    reading_pulse_freq_sweeping=reading_pulse_freq_sweeping.to_numpy()
                    frequency_scale[index,:,0]=time_scale[index,:,0]/(reading_pulse_duation*1e-3)*reading_pulse_freq_sweeping
for index in range(burn_and_burn_back_index_len):
        fig, ax=plt.subplots()    
        ax.plot(frequency_scale[index,:,0],absorption_burn_and_burn_back_corrected[0,:,index],label="{}".format(burn_and_burn_back_csv_variable_num[index,0]))
        #ax.plot(frequency_scale[index,:,0],absorption_noBurning_corrected[0,:,index])
        #ax.plot(time_scale[index,:,0],absorption_Burning_corrected[index,:,0])
        #ax.set_xlabel('Time(s)')
        ax.set_xlabel('Frequency detuning (MHz)')
        ax.set_ylabel('OD')
        ax.legend(loc=1,title='Amplitude of reading-out pulse',fontsize='x-small',title_fontsize='x-small')
plt.show()         
test=0