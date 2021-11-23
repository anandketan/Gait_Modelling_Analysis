import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import floor
import time
from scipy.stats import circmean
from scipy.stats import circstd
from collections import deque
import os
import subprocess
import glob
from datetime import datetime


df = pd.read_csv('test_7_allSensorData_2021-11-11_15_26_30.csv')
df = df.loc[df['FlagN']==1]
# print(len(df))
# rates = []
# first = df['_Gtime'][0]
# count = 0
# for i in df['_Gtime']:
#     count+=1
#     if i - first > 100:
#         rate = 1000 * count/(i-first)
#         rates.append(rate)
#         print(rate)
#         first = i
#         count = 0
# plt.plot(rates)
# plt.plot(np.zeros(len(rates)))
# df.index = range(0, len(df))
# pitch = df['_BPitch']
# print(df)
# plt.plot(pitch,label='Pitch2')
# pitch = pitch[1:len(pitch):10]
# print(len(pitch))
# print(df_norm)
# Mean = df_norm['Mean']
# Gait_Cycle = df_norm['% Gait Cycle']
# Std_D = df_norm['SD']
# sampling_rate = len(df)/(df.iloc[-1]['time']-df['time'][0])
# sampling_rate2 = len(df)/(df.iloc[-1]['_Ntime']/1000-df['_Ntime'][0]/1000)
# print(sampling_rate, sampling_rate2)
# print(df['_Ntime'][0], df.iloc[-1]['_Ntime'], (df.iloc[-1]['_Ntime'] - df['_Ntime'][0])/1000)
# print(df['time'][0], df.iloc[-1]['time'], df.iloc[-1]['time'] - df['time'][0])

# plt.plot(pitch,label='Pitchdownsampled')
# plt.plot(df['_CPitch'],label='Pitch2')
# plt.plot(df['_Btime'],label='time1')
# plt.plot(df['_Ctime'],label='time2')
# plt.plot(df['time'],label='Time')
# plt.legend()
# plt.fill_between(Gait_Cycle, Mean-Std_D, Mean+Std_D, alpha=1, color='lightgrey', facecolor='lavender',label='Normative Standard deviation')
# print(df['FlagG'].value_counts())
# print(100 * df['FlagG'].value_counts().get(1,0) / df['FlagN'].value_counts().get(1,0))
# plt.plot(df['FlagG'])
# plt.plot(df['FlagN'])
# plt.show()
# print(time.time())
# time.sleep(2)
# print(time.time())
# print(datetime.now().date())
# s= 'xrightzxxcacac'
# if 'right' in s:
#     print('yes')
# else:
#     print('no')