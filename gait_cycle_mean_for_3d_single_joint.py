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
from scipy import interpolate

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
    # plt.plot(alist)
    l = int(window_size/2)
    # print(l)
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
    # plt.plot(rolled_avg)
    # plt.show()
    return rolled_avg

def to_smooth(a,alist,window_size,times):
    x=alist
    for i in range(times):
        x=rolling_avg(a,x,window_size)
    return x


def pctDelay(knee_angle,column):
    # print(len(gait_reference))
    # print(len(knee_angle))
    # print(len(gait_cycle))

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
        print("No. of points in {}".format(i), len(cycles[i]))
        cycles[i] = [round(x, 3) for x in cycles[i]]
        if len(cycles[i]) != 1:
            cycles[i][-1] = 99.9
        try:
            f = interpolate.interp1d(cycles[i], data[i])
            xnew = np.linspace(cycles[i][0], cycles[i][-1], 1000)
            # xnew = np.linspace(0, 99.9, 1000)
            data[i] = f(xnew)
            cycles[i] = xnew
        except:
            pass
        plt.plot(cycles[i][:], data[i][:], alpha=0.6, color='#4287f5')
        # plt.show()
        print("No. of points in {}".format(i), len(cycles[i]))



    for i, dat in enumerate(data):
        init = dat[0]

    dict_comb = dict()
    for cycle, dat in zip(cycles, data):
        for i, j in zip(cycle, dat):
            if i in dict_comb.keys():
                dict_comb[i].append(j)
            else:
                dict_comb[i] = [j]

    # print("Dict comb:", dict_comb)

    sorted_dictcomb = sorted(dict_comb.items())
    timed_dict = dict(sorted_dictcomb)

    # print("Sorted dict comb:", timed_dict)

    time_aligned = pd.DataFrame.from_dict(timed_dict, orient='index').transpose()
    single_value_columns = [x for x in time_aligned.columns if len(time_aligned[x].unique()) <= 11]

    print("Number of DF columns:", len(time_aligned.columns))
    print("Time aligned DF:", time_aligned)
    # print("Value column check:", single_value_columns)

    ta = dict(time_aligned.mean())

    print("Time alogned dict:", ta)

    ta_list = list(ta.values())
    print(len(ta))
    print(ta)
    window_size = (len(ta) / 10) - (len(ta) / 10) % 10
    print(window_size)
    rolled_avg = rolling_avg(ta, ta_list, window_size)
    print("Rolling average:", rolled_avg)

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

    # print(len(value_ref))
    # print(len(data))
    # print(len(cycles))
    # print(len(rolled_avg))

    test_list = deque(rolled_avg)
    test_list.rotate(500)
    test_list = list(test_list)

    df_mean = pd.DataFrame(list(zip(list(ta.keys()), rolled_avg, rolled_avg_tdiff1, rolled_avg_tdiff2)),
                           columns=['pct_gait_cycle', 'Mean', 'minus_std', 'plus_std'])

    df_mean.to_csv(dest_dir + '\\' + '{}_mean_std.csv'.format(column))
    # for j in range(len(cycles)):#len(cycles)
    #     # print(len(data[j]))
    #     # print(len(value_ref[j]))
    #     # print(len(cycles[j]))
    #     plt.plot(cycles[j][:], data[j][:], alpha=0.6, color='#4287f5')
    #     # plt.show()
    #     # plt.plot(cycles[j][:], value_ref[j][:], alpha=0.6, color='green')
    #     # plt.title(j)
    #     # plt.savefig(dest_dir +"\\{}".format(j), bbox_inches='tight')
    #     # plt.show(block=False)
    #     # plt.pause(0.005)
    #     # plt.close()
    return ta, rolled_avg, test_list

files = []
for folder in os.listdir("DataFolder\\Testing\\2021-12-02"):
    files.append(folder.split("_")[1])
# column = input("Enter column name\n")
# joint = input("Enter joint\n")
for folder in os.listdir("DataFolder\\Testing\\2021-12-02"):
    joint = "Testing"
    # date = input("Enter date of trial in the format yyyy-mm-dd")
    date = "2021-12-02"
    # read_file = input("Enter file to be used \n")
    # trial = input("Enter trial to be used \n")
    read_file = folder
    # read_file = "Nikhil_1_gait_cycle"
    df = pd.read_csv("DataFolder\\"+joint + '\\'+date + '\\' +read_file+ '\\' +read_file+'.csv')
    df['flex_angle'] = rolling_avg_padded_zeros(list(df['flex_angle']), list(df['flex_angle']), 75)
    df['flex_angle'] = rolling_avg_padded_zeros(list(df['flex_angle']), list(df['flex_angle']), 75)
    df['var_angle'] = rolling_avg_padded_zeros(list(df['var_angle']), list(df['var_angle']), 75)
    df['var_angle'] = rolling_avg_padded_zeros(list(df['var_angle']), list(df['var_angle']), 75)
    df['rot_angle'] = rolling_avg_padded_zeros(list(df['rot_angle']), list(df['rot_angle']), 75)
    df['rot_angle'] = rolling_avg_padded_zeros(list(df['rot_angle']), list(df['rot_angle']), 75)
    print(df['flex_angle'].head(75))
    # df = pd.read_csv("DataFolder\\"+joint + '\\' +'Raafay_1_gait_cycle.csv')
    print("++++++",df.loc[df['alt_gait_cycle']==1].index[0])
    # df.drop(df.index[range(df.loc[df['alt_gait_cycle']==1].index[0])], inplace=True)
    df.index = range(0,len(df))
    # df['alt_gait_cycle'] = df['alt_gait_cycle'].round(3)

    gait_cycle = df['alt_gait_cycle']
    # knee_angle = df[column]
    gait_reference = df['hs']
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(date), '{}'.format(read_file))
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass # already exists

    # numberOfJoints = int(input("Enter no. of Joints"))
    columns = ['flex_angle','var_angle','rot_angle']
    labels = {'flex_angle':'Flexion_Extension', 'var_angle':'Valgus_Varus', 'rot_angle':'Rotation'}
    for column in columns:
        print(column)
        knee_angle = df[column]
        TimeAligned,RolledAvg,ShiftedRolledAvg = pctDelay(knee_angle,column)
        plt.plot(list(TimeAligned.keys()), RolledAvg, label='{}'.format(labels[column]), color = 'red')
        plt.title('{} Trial-{} {}'.format(read_file.split("_")[0],read_file.split("_")[1],labels[column]))
        plt.savefig(dest_dir +"\\{}".format(labels[column]), bbox_inches='tight')
        plt.legend()
        plt.show(block=False)
        plt.pause(0.005)
        # plt.show()
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