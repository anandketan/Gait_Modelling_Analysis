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

# new = pd.read_csv(r'C:\Users\Admin\Desktop\SystemModelling_GaitAnalysis\DataFolder\tester\2021-12-15\angle_1_gait_cycle\diff_pitch_angle_1.csv')
# plt.plot(new['Roll1'],label ='C Roll after correction')
# plt.plot(new['Roll2'],label ='D Roll after correction')
# plt.plot(new['flex_angle'],label ='flex_angle')

# df2 = pd.read_csv(r'Stitched_data_Nikhil_2021-11-23.csv')
df = pd.read_csv(r'C:\Users\Admin\Desktop\SystemModelling_GaitAnalysis\DataFolder\Treadmill\2021-12-16\Rashmi_1_gait_cycle\diff_pitch_Rashmi_1.csv')
# df2 = pd.read_csv(r'C:\Users\Admin\Desktop\SystemModelling_GaitAnalysis\DataFolder\Treadmill\2021-12-15\Raafay_1_gait_cycle\diff_pitch_Raafay_1.csv')
fauzan = pd.read_csv(r'C:\Users\Admin\Desktop\SystemModelling_GaitAnalysis\DataFolder\Treadmill\2021-12-16\Rashmi_1_gait_cycle\Rashmi_1_allSensorData_2021-12-16_12_24_39.csv')
print(fauzan.columns)
# raafay = pd.read_csv(r'C:\Users\Admin\Desktop\SystemModelling_GaitAnalysis\DataFolder\Treadmill\2021-12-15\Raafay_1_gait_cycle\Raafay_1_allSensorData_2021-12-15_12_21_57.csv')
# print(df.columns)
# df3 = df2.loc[(df2['FlagD']==1) & (df2['FlagC']==1)]
# df4 = df.iloc[df3.index]
# df4.reset_index(inplace=True)
# df4.to_csv('diff_pitch_test_1.csv')
# print(len(df3))
# print(len(df4))
# plt.plot(50*df['_AHS'], label = 'hs')
# plt.plot(df['_ADist'], label = 'dist')
# plt.plot(range(0,len(df4['flex_angle'])),df4['flex_angle'])
# print(fauzan.loc[21705, 'time'])
# print(fauzan.loc[399553, 'time'])
# print(fauzan.loc[421256, 'time'] - fauzan.loc[21705, 'time'], 421256-21705)
# print(raafay.loc[321323, 'time'] - raafay.loc[42126, 'time'], 321323-42126)

plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], fauzan['rate'][21705:421256], label ='rate')
plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], df['flex_angle'][21705:421256], label ='flex_angle(difference)')
# plt.plot(raafay['time'][21705:421256] - raafay['time'][21705], raafay['_CRollQ'][21705:421256], label ='C Roll')
# plt.plot(raafay['time'][21705:421256] - raafay['time'][21705], raafay['_DRollQ'][21705:421256], label ='D Roll')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], df['Roll1'][21705:421256],label ='C Roll after correction')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], df['Roll2'][21705:421256],label ='D Roll after correction')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], fauzan['GyroX_D'][21705:421256],label ='AccX_D')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], fauzan['GyroY_D'][21705:421256],label ='AccY_D')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], fauzan['GyroZ_D'][21705:421256],label ='AccZ_D')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], fauzan['GyroX_C'][21705:421256],label ='AccX_C')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], fauzan['GyroY_C'][21705:421256],label ='AccY_C')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705], fauzan['GyroZ_C'][21705:421256],label ='AccZ_C')
# plt.plot([-180]* 650,label ='-180')
# plt.plot([180]* 650,label ='180')
# plt.plot([-170]* 650,label ='-170')
# plt.plot([170]* 650,label ='170')
# plt.plot(fauzan['time'][21705:421256] - fauzan['time'][21705],df['hs'][21705:421256], label = 'FauzanHS')
# plt.plot(raafay['time'][42126:321323] - raafay['time'][42126], df2['flex_angle'][42126:321323])
# plt.plot(df2['hs'], label = 'RaafayHS')
# plt.plt
plt.legend()
plt.show()
# df = df.loc[df['FlagN']==1]
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