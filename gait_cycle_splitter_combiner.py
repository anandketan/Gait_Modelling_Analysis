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

def get_normative(file="KneeFlexExt.csv"):
    df_norm = pd.read_csv(file)
    Mean = df_norm['Mean']
    Gait_Cycle = df_norm['% Gait Cycle']
    Std_D = df_norm['SD']
    return Mean, Gait_Cycle, Std_D


def rolling_avg(a,alist,window_size):
    l = int(window_size/2)
    print(l)
    # before = alist[0]
    before = alist[-(l-1):]
    # after = alist[-1]
    after = alist[:l]
    # alist = [before]*(l-1) + alist + [after]*l
    alist = before + alist + after
    rolled_avg = [0]*len(a)
    j=0
    for i,n in enumerate(alist):
        if i>=(l-1) and i<len(alist)-l:
            rolled_avg[j] = sum(alist[i-l+1:i+l+1])/window_size
            # rolled_avg[j] = circmean(alist[i-l+1:i+l+1], high=high, low=low,nan_policy='omit')
            j+=1
    return rolled_avg

def rolling_avg_padded_zeros(a,alist,window_size):
    l = int(window_size/2)
    print(l)
    before = alist[0]
    # before = alist[-(l-1):]
    after = alist[-1]
    # after = alist[:l]
    alist = [before]*(l-1) + alist + [after]*l
    # alist = before + alist + after
    rolled_avg = [0]*len(a)
    j=0
    for i,n in enumerate(alist):
        if i>=(l-1) and i<len(alist)-l:
            rolled_avg[j] = sum(alist[i-l+1:i+l+1])/window_size
            # rolled_avg[j] = circmean(alist[i-l+1:i+l+1], high=high, low=low,nan_policy='omit')
            j+=1
    return rolled_avg


def pctDelay(knee_angle,column):
    print(len(gait_reference))
    print(len(knee_angle))
    print(len(gait_cycle))

    n = 0  # nth cycle
    temp = []
    data = []  # all angle data
    rate = []
    cycles = []  # all cycles
    temp_ref = []
    value_ref = []

    for i in range(gait_cycle.shape[0]):
        if (gait_cycle[i].is_integer()):
            n = int(gait_cycle[i])
            if rate:
                cycles.append(rate)
                data.append(temp)
                value_ref.append(temp_ref)
                rate = []
                temp = []
                temp_ref = []
                rate.append((gait_cycle[i] - n) * 100)
                temp.append(knee_angle[i])
                temp_ref.append(gait_reference[i])
            else:
                rate.append((gait_cycle[i] - n) * 100)
                temp.append(knee_angle[i])
                temp_ref.append(gait_reference[i])
        else:
            rate.append((gait_cycle[i] - n) * 100)
            temp.append(knee_angle[i])
            temp_ref.append(gait_reference[i])

    if rate:
        cycles.append(rate)
        data.append(temp)
        value_ref.append(temp_ref)

    for i, (cycle, dat) in enumerate(zip(cycles, data)):
        cycles[i] = [round(x, 3) for x in cycles[i]]

    for i, dat in enumerate(data):
        init = dat[0]

    dict_comb = dict()
    ix = 0
    colors = ['red', 'blue', 'green']
    for cycle, dat in zip(cycles, data):
        if ix < 3:
            plt.plot(cycle, dat, color = colors[ix], label='gait cycle {}'.format(ix+1))
            plt.plot([dat[0]]*101, '--', color = colors[ix])
            plt.title('Superimposed Gait Cycles')
            plt.xlabel("% Gait Cycle")
            plt.ylabel("Degrees")
        ix+=1
        for i, j in zip(cycle, dat):
            if i in dict_comb.keys():
                dict_comb[i].append(j)
            else:
                dict_comb[i] = [j]

    plt.legend()
    plt.show()

    sorted_dictcomb = sorted(dict_comb.items())
    timed_dict = dict(sorted_dictcomb)

    time_aligned = pd.DataFrame.from_dict(timed_dict, orient='index').transpose()
    single_value_columns = [x for x in time_aligned.columns if len(time_aligned[x].unique()) == 2]

    ta = dict(time_aligned.mean())

    ta_list = list(ta.values())
    print(len(ta))
    window_size = (len(ta) / 10) - (len(ta) / 10) % 10
    print(window_size)
    rolled_avg = rolling_avg(ta, ta_list, window_size)

    ta_std = time_aligned.std()
    for i in single_value_columns:
        ta_std[i] = 0
    ta_diff1 = rolled_avg - ta_std
    ta_diff2 = rolled_avg + ta_std
    tdiff1list = list(dict(ta_diff1).values())
    tdiff2list = list(dict(ta_diff2).values())
    # print(tdiff1list)

    rolled_avg_tdiff1 = rolling_avg(ta, tdiff1list, window_size)
    rolled_avg_tdiff2 = rolling_avg(ta, tdiff2list, window_size)

    print(len(value_ref))
    print(len(data))
    print(len(cycles))
    print(len(rolled_avg))

    test_list = deque(rolled_avg)
    test_list.rotate(500)
    test_list = list(test_list)

    df_mean = pd.DataFrame(list(zip(list(ta.keys()), rolled_avg, rolled_avg_tdiff1, rolled_avg_tdiff2)),
                           columns=['pct_gait_cycle', 'Mean', 'minus_std', 'plus_std'])

    # df_mean.to_csv(dest_dir + '\\' + '{}mean_std.csv'.format(column))
    return ta, rolled_avg, test_list, ta_list


# column = input("Enter column name\n")
# joint = input("Enter joint\n")
# for i in [6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 35,  37, 38, 39, 40, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]:
joint = "right_knee"
# date = input("Enter date of trial in the format yyyy-mm-dd")
date = "2021-11-23"
# read_file = input("Enter file to be used \n")
# trial = input("Enter trial to be used \n")
read_file = "Nikhil_{}_gait_cycle".format(7)
df = pd.read_csv("DataFolder\\"+joint + '\\'+date + '\\' +read_file+ '\\' +read_file+'.csv')
df['flex_angle'] = rolling_avg_padded_zeros(list(df['flex_angle']),list(df['flex_angle']),75)
# df['flex_angle'] = rolling_avg_padded_zeros(list(df['flex_angle']),list(df['flex_angle']),75)
df['var_angle'] = rolling_avg_padded_zeros(list(df['var_angle']),list(df['var_angle']),75)
df['rot_angle'] = rolling_avg_padded_zeros(list(df['rot_angle']),list(df['rot_angle']),75)
# df = df.loc[df['alt_gait_cycle']<=3]
plt.plot(df['alt_gait_cycle'],df['flex_angle'], label="Flexion angle", color='grey')
plt.plot([0,1,2,3],[df.loc[df['alt_gait_cycle']==0]['flex_angle']]*4, '--', color = 'red', label = 'Start of 1st gait cycle')
plt.scatter(0,df.loc[df['alt_gait_cycle']==0]['flex_angle'], color = 'red')
plt.plot([1,2,3],[df.loc[df['alt_gait_cycle']==1]['flex_angle']]*3, '--', color = 'blue', label = 'Start of 2nd gait cycle(End of 1st)')
plt.scatter(1,df.loc[df['alt_gait_cycle']==1]['flex_angle'], color = 'blue')
plt.plot([2,3],[df.loc[df['alt_gait_cycle']==2]['flex_angle']]*2, '--', color = 'green', label = 'Start of 3rd gait cycle(End of 2nd)')
plt.scatter(2,df.loc[df['alt_gait_cycle']==2]['flex_angle'], color = 'green')
plt.title("Flexion/Extension vs. Time")
plt.xlabel("Time")
plt.ylabel("Degrees")
plt.legend()
plt.show()
# df = pd.read_csv("DataFolder\\"+joint + '\\' +'Raafay_1_gait_cycle.csv')
print("++++++",df.loc[df['alt_gait_cycle']==1].index[0])
# df.drop(df.index[range(df.loc[df['alt_gait_cycle']==1].index[0])], inplace=True)
df.index = range(0,len(df))
df['alt_gait_cycle'] = df['alt_gait_cycle'].round(3)

gait_cycle = df['alt_gait_cycle']
# knee_angle = df[column]
gait_reference = df['hs']
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(datetime.now().date()), '{}'.format(read_file))
try:
    os.makedirs(dest_dir)
except OSError:
    pass # already exists

# numberOfJoints = int(input("Enter no. of Joints"))
columns = ['flex_angle','var_angle','rot_angle']
labels = {'flex_angle':'Flexion_Extension', 'var_angle':'Valgus_Varus', 'rot_angle':'Rotation'}
for column in columns:
    print(column)
    knee_angle = list(df[column])
    print("Here:",len(knee_angle))
    TimeAligned,RolledAvg,ShiftedRolledAvg,Original = pctDelay(knee_angle,column)
    # plt.plot(list(TimeAligned.keys()), RolledAvg, label='Right Knee {}'.format(labels[column]))
    plt.plot(list(TimeAligned.keys()), RolledAvg, label='Flexion angle', color='grey')
    plt.plot([RolledAvg[0]]*101, '--', label = 'start/end', color = 'orange')
    # plt.plot(list(TimeAligned.keys()), Original, label='Right Knee {}'.format(labels[column]))
    # plt.title('Right Knee {}'.format(labels[column]))
    plt.xlabel("% Gait Cycle")
    plt.ylabel("Degrees")
    plt.title("Averaged Gait cycle")
    # plt.savefig(dest_dir +"\\Right Knee {}".format(labels[column]), bbox_inches='tight')
    plt.legend()
    plt.show()
    plt.close()


# plt.plot(Gait_Cycle,Mean,color='navy',label='Normative mean')
# plt.fill_between(Gait_Cycle, Mean-Std_D, Mean+Std_D, alpha=1, color='lightgrey', facecolor='lavender',label='Normative Standard deviation')

# plt.plot(list(ta.keys()),rolled_avg,color='red',label='Mean')
# plt.scatter(list(ta.keys()),rolled_avg,color='red',label='Mean')
# plt.plot(list(ta.keys()),test_list,color='green',label='Mean_shift')
# plt.plot(list(ta.keys()),rolled_avg_tdiff1, color='orange')
# plt.plot(list(ta.keys()),rolled_avg_tdiff2, color='green')
# # plt.fill_between(list(ta.keys()), rolled_avg_tdiff1, rolled_avg_tdiff2, color='grey', label='Standard deviation')
# plt.title("{} Flexion/Extension".format(joint))
# plt.legend()
# plt.show()