# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 20:20:50 2022

@author: wj2002
"""

import os
import numpy as np
import pandas as pd
from natsort import natsorted
import matplotlib.pyplot as plt
import sys

# Directory and folder for data
dir = 'C:\\Users\\wj2002\\Dropbox (Heriot-Watt University Team)\\RES_EPS_Quantum_Photonics_Lab\\Experiments\\Current Experiments\\Broadband telecom quantum memories\\Pr_YSO_spectroscopy_HWU'
folder = '20220927_Pr_YSO_AFC'

path = dir + '\\' + folder + '\\'

data_file='AFC92707'
ref_file ='AFC92706'

read_data=pd.read_csv(os.path.join(path,data_file +'.'+'csv'))
read_ref=pd.read_csv(os.path.join(path,ref_file +'.'+'csv'))

data=read_data.to_numpy()
ref=read_ref.to_numpy()

data_corrected=data[:,2]-min(data[:,2])+0.000001
ref_corrected=ref[:,2]-min(ref[:,2])+0.000001

absorption=np.log(ref[:,2]/data[:,2])
absorption_corrected=np.log(ref_corrected/data_corrected)

time=data[:,0]
frequency=time/(4*1e-3)*20

plt.plot(frequency,absorption_corrected)


