# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 22:40:54 2022

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
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import Defined_functions as DF
import sys

# directory and folder for images
dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU'
folder = '20220614_Pr_YSO_spectral_hole_burning_optimisation'

path = dir + '\\' + folder + '\\'
file_list = os.listdir(path)

list_csv=natsorted([i for i in file_list if i.endswith('.CSV')])

list_xlsx=natsorted([i for i in file_list if i.endswith('.xlsx')])
if not list_xlsx:
        sys.exit('Excel file does not exist or must be of format ".xlsx"')
xlsx = pd.ExcelFile(path + list_xlsx[0])
print(list_xlsx[0])
#Finding out reference
read_xlsx= pd.read_excel(xlsx, sheet_name='Sheet1')
read_flag= pd.read_excel(xlsx, sheet_name='Sheet1', usecols=['Flag'])
flagNum = np.reshape(read_flag.to_numpy(), len(read_flag))
xlsx_size=read_xlsx.shape

find_reference=np.where(flagNum == 1)
reference_index=find_reference[-1]
ref_csv=read_xlsx.loc[reference_index]
ref_csv_name=pd.DataFrame(ref_csv, columns= ['File name'])
ref_csv_name_1=ref_csv_name.to_numpy()
ref_csv_name=str(ref_csv_name_1[0,0])
read_ref_data=pd.read_csv(os.path.join(path,ref_csv_name+'.'+'csv'))
ref_data=read_ref_data.to_numpy()
ref_data_corrected=ref_data[:,2]-min(ref_data[:,2])+0.0000001
time_scale=ref_data[:,0]
time_scale_len=len(time_scale)
plt.figure(1)
plt.plot(time_scale,ref_data[:,2])
plt.plot(time_scale,ref_data_corrected)

find_NoBurning=np.where(flagNum == 2)
NoBurning_index=find_NoBurning[-1]
NoBurning_csv=read_xlsx.loc[NoBurning_index]
NoBurning_csv_name=pd.DataFrame(NoBurning_csv, columns= ['File name'])
NoBurning_csv_name_1=NoBurning_csv_name.to_numpy()
NoBurning_csv_name=str(NoBurning_csv_name_1[0,0])
read_NoBurning_data=pd.read_csv(os.path.join(path,NoBurning_csv_name +'.'+'csv'))
NoBurning_data=read_NoBurning_data.to_numpy()
NoBurning_data_corrected=NoBurning_data[:,2]-min(NoBurning_data[:,2])+0.0000001

plt.figure(2)
plt.plot(time_scale,NoBurning_data[:,2])
plt.plot(time_scale,NoBurning_data_corrected)

absorption_NonBurning=np.log(ref_data_corrected/NoBurning_data_corrected)

plt.figure(3)
plt.plot(time_scale,absorption_NonBurning)

find_Burning=np.where(flagNum == 0)
Burning_index=np.transpose(np.array(find_Burning))
Burning_index_len=len(Burning_index)
Burning_csv=np.zeros([Burning_index_len,xlsx_size[1]],dtype=np.int64)
#Burning_csv=Burning_csv.to_frame()
Burning_data=np.empty([Burning_index_len,time_scale_len,4])
Burning_data_corrected=np.empty([Burning_index_len,time_scale_len,1])
absorption_Burning=np.empty([Burning_index_len,time_scale_len,1])

for index in range(Burning_index_len):
    
    Burning_csv=read_xlsx.loc[index]
    Burning_csv=Burning_csv.to_frame()
    Burning_csv=Burning_csv.T
    Burning_csv_name=pd.DataFrame(Burning_csv, columns= ['File name'])
    Burning_csv_name_1=Burning_csv_name.to_numpy()
    Burning_csv_name=str(Burning_csv_name_1[0,0])
    read_Burning_data=pd.read_csv(os.path.join(path,Burning_csv_name +'.'+'csv'))
    Burning_data[index,:,:]=read_Burning_data.to_numpy()
    Burning_data_corrected[index,:,0]=Burning_data[index,:,2]-min(Burning_data[index,:,2])+0.0000001
    
    absorption_Burning[index,:,0]=np.log(ref_data_corrected/Burning_data_corrected[index,:,0])

    fig, ax=plt.subplots()
    ax.plot(time_scale,absorption_Burning[index,:,0])
    ax.set_xlabel('Time(s)')
    ax.set_ylabel('Amplitude(V)')
    ax.legend()
    
    print(index)
    flag=0


'''
for index, ref_num in enumerate(flagNum):
    if ref_num == 1:
        ref_csv_name=read_xlsx.loc[index]
        read_ref_data=pd.read_csv(os.path.join(path,ref_csv_name['File name']+'.'+'csv'))
        ref_data=read_ref_data.to_numpy()
    elif ref_num == 2:
        NoBurning_csv_name=read_xlsx.loc[index]
        read_NoBurning_data=pd.read_csv(os.path.join(path,NoBurning_csv_name['File name']+'.'+'csv'))
        NoBurning_data=read_NoBurning_data.to_numpy()
        absorption_NonBurning=np.log(ref_data[:,2]/NoBurning_data[:,2])
'''            
flag=1
#list_csv=DF.list_dir_csv(file_dir=path)
#list_csv_length=int(len(list_csv))
#print(list_csv)

#dirname_csv=list(range(list_csv_length))
#filename_csv=list(range(list_csv_length))
#for index,file in enumerate(list_csv):
#    dirname_csv[index],filename_csv[index] = os.path.split(list_csv[index])

#list_xlsx=DF.list_dir_xlsx(file_dir=path)