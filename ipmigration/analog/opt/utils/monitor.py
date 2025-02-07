#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 19:05:15 2025

@author: leiyuan
"""

import math
import time
import datetime

import matplotlib
from matplotlib import pyplot as plt
import numpy as np
matplotlib.use('QtAgg')
#%matplotlib qt5#在spyder等集成开发环境中改为matplotlib.use('QtAgg')
#PyQt5_Qt5-5.15.16-py3-none-manylinux2014_x86_64.whl 
# pip3 install PySide2
# pip3 install PyQt5


# plt.close()


class Monitor:
    def __init__(self, save_dir, target_df):
        row = 4
        self.num_targets = target_df.shape[0]
        col = math.ceil(self.num_targets/row)
        self.subp = str(row)+str(col)
        
        self.start_time = time.time()
        
        self.y_labels = [] 
        self.y_data = []
        self.x_data = []
        for i,r in target_df.iterrows():
            self.y_labels.append(r['Details'])
            self.y_data.append([])
        
        plt.ion()
        plt.figure(figsize =(20,20))
        

        
        
        
    def update(self, data):
        self.x_data.append(len(self.x_data) + 1)
        run_time =  str(datetime.timedelta(seconds=int(time.time()-self.start_time)))
        plt.clf()  #
        for i in range(self.num_targets): 
            plt.suptitle("Run Time : %s"%(run_time), size=16)
            self.y_data[i].append(data[i])
            subp = int(self.subp + str(i+1))
            plt.subplot(subp)
            plt.ylabel(self.y_labels[i])
            # plt.text(-5, 60, self.y_labels[i] + ':'+ str(data[i]), fontsize = 10)
            plt.title(self.y_labels[i])
            plt.plot(self.x_data,self.y_data[i])
            plt.ioff()  # 关闭画图窗口
            plt.pause(0.001)

    def save(self):
        pass

# #test
# import pandas as pd
# df = pd.read_csv('./demo/analog_opt/opamp/setting_outputs.csv')
# mon = Monitor('./demo/analog_opt/opamp/output', df)

# for i in range(10):
#     data = [1,1,1,1,1,1,1,1]
#     data = [t+i for t in data]
#     time.sleep(0.5)
#     mon.update(data)
    
    