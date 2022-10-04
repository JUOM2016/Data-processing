# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 23:03:58 2022

@author: Wei Jiang

Functions used for the spectral hole burning (spectral window) data processing
"""
import os

def list_dir_csv(file_dir):
    list_csv=[]
    dir_list=os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir, cur_file)
        if os.path.isdir(path):
             print("{0}:is a folder!".format(cur_file))
        if os.path.isfile(path):
             print("{0}:is file!".format(cur_file))
        if os.path.splitext(cur_file)[1] =='.CSV':
             csv_file=os.path.join(file_dir, cur_file)
             print(csv_file)
             list_csv.append(csv_file)
    return list_csv

def list_dir_xlsx(file_dir):
    list_xlsx=[]
    dir_list=os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir, cur_file)
        if os.path.isdir(path):
             print("{0}:is a folder!".format(cur_file))
        if os.path.isfile(path):
             print("{0}:is file!".format(cur_file))
        if os.path.splitext(cur_file)[1] =='.xlsx':
             xlsx_file=os.path.join(file_dir, cur_file)
             print(xlsx_file)
             list_xlsx.append(xlsx_file)
    return list_xlsx