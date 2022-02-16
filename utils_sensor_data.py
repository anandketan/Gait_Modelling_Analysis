import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import socket
import time
import math
import datetime
from datetime import datetime
import os
import keyboard
from scipy import interpolate
from collections import deque


def correctYaw(prev_yaw, yaw, n):
    if prev_yaw >= 160 and prev_yaw <= 180 and float(yaw) >= -180 and float(yaw) <= -160:
        n += 1
    elif float(yaw) >= 160 and float(yaw) <= 180 and prev_yaw >= -180 and prev_yaw <= -160:
        n -= 1

    prevyawnew = float(yaw)
    # print(nC, pitch, prevaccC, d['C'][az])
    yawnew = n * 360 + float(yaw)
    return prevyawnew, yawnew, n


def correctRoll(prev_roll, roll, n):
    if prev_roll >= 160 and prev_roll <= 180 and float(roll) >= -180 and float(roll) <= -160:
        n += 1
    elif float(roll) >= 160 and float(roll) <= 180 and prev_roll >= -180 and prev_roll <= -160:
        n -= 1

    prevrollnew = float(roll)
    # print(nC, pitch, prevaccC, d['C'][az])
    rollnew = n * 360 + float(roll)
    return prevrollnew, rollnew, n


def correctPitch(prev_pitch, pitch, n):
    prevpitchnew = float(pitch)
    pitchnew = float(pitch)
    return prevpitchnew, pitchnew, n


def anklecalibration(anglesum, calibrationcounter, side, segment):
    calibAngle = anglesum/calibrationcounter
    print("Initial {} {} angle:".format(side, segment), calibAngle)
    calibAngle = -180 - calibAngle
    print("{} {} calibration angle:".format(side, segment), calibAngle)
    return calibAngle


def add_gait_cycle(dest_path="", read_path="", joint="", hstype=1):

    if dest_path == "":
        dest_path = input("Enter destination path with .csv extension\n")

    if read_path == "":
        read_path = input("Enter read path without using .csv extension\n")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}.csv'.format(read_path))

    df = pd.read_csv(read_path)[:]  # replace with path to any csv with pressure sensor data
    df.index = range(0, len(df))

    if hstype:
        h = 'hs'
    else:
        h = 'hs_US'

    df['Ps3prev'] = df[h].shift(1)  # 'Ps3' to be changed to column name of pressure sensor data in csv
    df['Gait_cycle'] = [0]*len(df)
    df['Gait_cycle'] = (df[h] >= 100) & (df['Ps3prev'] < 100)
    df['Gait_cycle'].replace([np.nan, False, True], [0, 0, 1], inplace=True)
    last = df.loc[df['Gait_cycle'] == 1].index
    df.loc[df['Gait_cycle'] == 1, 'Gait_cycle'] = np.arange(1, df['Gait_cycle'].value_counts()[1]+1, 1)

    starts = df.loc[df['Gait_cycle'] != 0]
    x = 0
    for i in starts['Gait_cycle'][:-1]:
        x = 1/((df.loc[df['Gait_cycle'] == (i+1)].index - df.loc[df['Gait_cycle'] == i].index)[0])
        fill = np.linspace(i+x, i+1-x, (df.loc[df['Gait_cycle'] == (i+1)].index - df.loc[df['Gait_cycle'] == i].index)[0]-1)
        df.loc[df.loc[df['Gait_cycle'] == i].index[0]+1:df.loc[df['Gait_cycle'] == (i+1)].index[0]-1, 'Gait_cycle'] = fill

    n = starts['Gait_cycle'][-1:].values[0]
    i = starts['Gait_cycle'][-1:].index[0]
    j = df.iloc[-1].name

    fill = np.linspace(n+x, n+(j-i)*x, j-i)  # last cycle filled with steps from previous cycle since it is not complete

    df.loc[i+1:j, 'Gait_cycle'] = fill

    print(df.index)
    print(last[-1])
    df = df.loc[:last[-1]]
    df = df.drop(range(0, df.loc[df['Gait_cycle'] == 1].index[0]))  # drops everything before the start of the first cycle

    df['alt_gait_cycle'] = df['Gait_cycle'] - 1  # starts cycle numbering from 0 instead of 1

    df.to_csv(dest_path)  # destination path

    return dest_path


def get_normative(file="KneeFlexExt.csv"):
    df_norm = pd.read_csv(file)
    Mean = df_norm['Mean']
    Gait_Cycle = df_norm['% Gait Cycle']
    Std_D = df_norm['SD']
    return Mean, Gait_Cycle, Std_D


def rolling_avg(a, alist, window_size):
    l = int(window_size/2)
    print(l)
    # before = alist[0]
    before = alist[-(l-1):]
    # after = alist[-1]
    after = alist[:l]
    # alist = [before]*(l-1) + alist + [after]*l
    print(before)
    print(after)
    print(alist)
    print(type(alist))
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    alist = before + alist + after
    rolled_avg = [0]*len(a)
    j = 0
    for i, n in enumerate(alist):
        if i >= (l-1) and i < len(alist)-l:
            rolled_avg[j] = sum(alist[i-l+1:i+l+1])/window_size
            # rolled_avg[j] = circmean(alist[i-l+1:i+l+1], high=high, low=low,nan_policy='omit')
            j += 1
    return rolled_avg


def rolling_avg_padded_zeros(a, alist, window_size):
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
    j = 0
    for i, n in enumerate(alist):
        if i >= (l-1) and i < len(alist)-l:
            rolled_avg[j] = sum(alist[i-l+1:i+l+1])/window_size
            # rolled_avg[j] = circmean(alist[i-l+1:i+l+1], high=high, low=low,nan_policy='omit')
            j += 1
    # plt.plot(rolled_avg)
    # plt.show()
    return rolled_avg


def to_smooth(a, alist, window_size, times):
    x = alist
    for i in range(times):
        x = rolling_avg(a, x, window_size)
    return x


def pctDelay(knee_angle, column, gait_cycle, gait_reference, dest_dir):
    n = 0  # nth cycle
    temp = []
    data = []  # all angle data
    rate = []
    cycles = []  # all cycles
    temp_ref = []
    value_ref = []

    for i in range(gait_cycle.shape[0]):
        if gait_cycle[i].is_integer():
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

    # for i, (cycle, dat) in enumerate(zip(cycles, data)):
    #     cycles[i] = [round(x, 3) for x in cycles[i]]

    for i, (cycle, dat) in enumerate(zip(cycles, data)):
        print("No. of points in {}".format(i), len(cycles[i]))
        cycles[i] = [round(x, 3) for x in cycles[i]]
        if len(cycles[i]) != 1:
            cycles[i][-1] = 99.9
        plt.plot(cycles[i][:], data[i][:], alpha=0.6, color='red')
        try:
            f = interpolate.interp1d(cycles[i], data[i])
            xnew = np.linspace(cycles[i][0], cycles[i][-1], 1000)
            # xnew = np.linspace(0, 99.9, 1000)
            data[i] = list(f(xnew))
            cycles[i] = list(xnew)
            window_size_cycle = ((len(cycles[i]) / 10) - (len(cycles[i]) / 10) % 10) / 2
            data[i] = rolling_avg(cycles[i], data[i], window_size_cycle)
            data[i] = rolling_avg(cycles[i], data[i], window_size_cycle)
            plt.plot(cycles[i][:], data[i][:], alpha=0.6, color='blue')
            plt.title("{}-{}".format(column, i))
            plt.savefig(dest_dir + "\\" + column + "\\{}".format(i), bbox_inches='tight')
            plt.show(block=False)
            plt.pause(0.005)
            plt.close()
        except:
            pass
        print("No. of points in {} after interpolation".format(i), len(cycles[i]))

    for i, dat in enumerate(data):
        init = dat[0]

    dict_comb = dict()
    for cycle, dat in zip(cycles, data):
        for i, j in zip(cycle, dat):
            if i in dict_comb.keys():
                dict_comb[i].append(j)
            else:
                dict_comb[i] = [j]

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

    # print(len(value_ref))
    # print(len(data))
    # print(len(cycles))
    # print(len(rolled_avg))

    test_list = deque(rolled_avg)
    test_list.rotate(500)
    test_list = list(test_list)

    df_mean = pd.DataFrame(list(zip(list(ta.keys()), rolled_avg, test_list, rolled_avg_tdiff1, rolled_avg_tdiff2)),
                           columns=['pct_gait_cycle', 'Mean', 'meanShifted50pct','minus_std', 'plus_std'])
    # print(knee_angle)
    # df_mean.to_csv(dest_dir + '\\' + knee_angle + 'mean_std.csv')
    df_mean.to_csv(dest_dir + '\\' + '{}_mean_std.csv'.format(column))
    for j in range(len(cycles)):  # len(cycles)
        # print(len(data[j]))
        # print(len(value_ref[j]))
        # print(len(cycles[j]))
        # plt.plot(cycles[j][:], data[j][:], alpha=0.6, color='#4287f5')
        # plt.show()
        plt.plot(cycles[j][:], data[j][:], alpha=1, color='blue')
    plt.title("{}-All".format(column))
    plt.savefig(dest_dir + "\\" + column + "\\All", bbox_inches='tight')
    plt.show(block=False)
    plt.pause(0.005)
    plt.close()
    return ta, rolled_avg, test_list
