import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import floor



df_norm = pd.read_csv('KneeFlexExt.csv')
# print(df_norm)
norm_Mean = df_norm['Mean']
norm_Gait_Cycle = df_norm['% Gait Cycle']
norm_Std_D = df_norm['SD']


df_mean1 = pd.read_csv('rashmisecondabs1mean_std.csv')
Mean1 = df_mean1['Mean']
Gait_Cycle1 = df_mean1['pct_gait_cycle']
plus_std1 = df_mean1['plus_std']
minus_std1 = df_mean1['minus_std']

df_mean2 = pd.read_csv('rashmisecondabs2mean_std.csv')
Mean2 = df_mean2['Mean']
Gait_Cycle2 = df_mean2['pct_gait_cycle']
plus_std2 = df_mean2['plus_std']
minus_std2 = df_mean2['minus_std']

df_mean3 = pd.read_csv('rashmisecondabs3mean_std.csv')
Mean3 = df_mean3['Mean']
Gait_Cycle3 = df_mean3['pct_gait_cycle']
plus_std3 = df_mean3['plus_std']
minus_std3 = df_mean3['minus_std']
#
# df_mean4 = pd.read_csv('nikhilfinalabs4mean_std.csv')
# Mean4 = df_mean4['Mean']
# Gait_Cycle4 = df_mean4['pct_gait_cycle']
# plus_std4 = df_mean4['plus_std']
# minus_std4 = df_mean4['minus_std']



plt.plot(norm_Gait_Cycle,norm_Mean,color='navy',label='Normative mean')
plt.fill_between(norm_Gait_Cycle, norm_Mean-norm_Std_D, norm_Mean+norm_Std_D, alpha=1, color='lightgrey', facecolor='lavender',label='Standard deviation')

plt.plot(Gait_Cycle1,Mean1,label='Rashminew1')
plt.plot(Gait_Cycle2,Mean2,label='Rashminew2')
plt.plot(Gait_Cycle3,Mean3,label='Rashminew3')
# plt.plot(Gait_Cycle4,Mean4,label='Nikhil4')
# plt.plot(Gait_Cycle1,Mean1,label='Rashmi')
# plt.plot(Gait_Cycle1,Mean1,label='Raafay')
plt.xlabel("% Gait Cycle")
plt.ylabel("Degrees")
plt.title("Ankle")
plt.axhline(y=0, color='k')
plt.legend()
plt.show()