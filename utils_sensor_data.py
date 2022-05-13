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


def correctPitch(prev_acc, cur_acc, pitch, n):
    if prev_acc > 0 and float(cur_acc) <= 0 and float(pitch) > 0:
        print("1st condition")
        n -= 1
    elif prev_acc > 0 and float(cur_acc) <= 0 and float(pitch) < 0:
        print("2nd condition")
        n += 1
    elif prev_acc <= 0 and float(cur_acc) > 0 and float(pitch) > 0:
        print("3rd condition")
        n += 1
    elif prev_acc <= 0 and float(cur_acc) > 0 and float(pitch) < 0:
        print("4th condition")
        n -= 1
    prevaccnew = float(cur_acc)
    pitchnew = n * 180 + math.pow(-1, n) * float(pitch)
    return prevaccnew, pitchnew, n


def anklecalibration(anglesum, calibrationcounter, side, segment):
    calibAngle = anglesum/calibrationcounter
    print("Initial {} {} angle:".format(side, segment), calibAngle)
    calibAngle = -180 - calibAngle
    print("{} {} calibration angle:".format(side, segment), calibAngle)
    return calibAngle

def initialangleaverage(anglesum, calibrationcounter, angle):
    calibAngle = anglesum/calibrationcounter
    print("Initial {} angle:".format(angle), calibAngle)
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

    if rate:
        cycles.append(rate)
        data.append(temp)
        value_ref.append(temp_ref)

    # for i, (cycle, dat) in enumerate(zip(cycles, data)):
    #     cycles[i] = [round(x, 3) for x in cycles[i]]

    for i, (cycle, dat) in enumerate(zip(cycles, data)):
        try:
            os.makedirs(os.path.join(dest_dir, "cycle_{}".format(i)))
        except OSError:
            pass
        print("No. of points in {}".format(i), len(cycles[i]))
        cycles[i] = [round(x, 3) for x in cycles[i]]
        if len(cycles[i]) != 1:
            cycles[i][-1] = 99.9
        fig = plt.figure(figsize=(19.2,10.8))
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
            test_list = deque(data[i])
            test_list.rotate(500)
            test_list = list(test_list)
            cycle_df = pd.DataFrame(list(zip(cycles[i], data[i], test_list)),
                columns=['pct_gait_cycle', 'Mean', 'meanShifted50pct'])
            cycle_df.to_csv(dest_dir + "\\" + column + '\\cycle_{}_mean_std.csv'.format(i))
            cycle_df.to_csv(dest_dir + "\\" + "cycle_{}".format(i) + '\\{}_mean_std.csv'.format(column))
            plt.plot(cycles[i][:], data[i][:], alpha=0.6, color='blue')
            plt.title("{}-{}".format(column, i))
            plt.savefig(dest_dir + "\\" + column + "\\{}".format(i), bbox_inches='tight')
            plt.savefig(dest_dir + "\\" + "cycle_{}".format(i) + "\\" + column, bbox_inches='tight')
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

def plt_averages(mainfolder, subfolder, date, foldername, jointname, dest_dir):
    folder = os.path.join(mainfolder, subfolder, date, foldername)
    index = [1, 3, 5, 2, 4, 6]
    i = 0

    fig = plt.figure(figsize=(19.2,10.8))
    # gs = fig.add_gridspec(3, 2, wspace=0.04)
    gs = fig.add_gridspec(3, 2, wspace=0.13, hspace=0.33)
    # axs = gs.subplots(sharex=True, sharey='row')
    axs = gs.subplots()
    # fig.suptitle("3d angles for both knees")
    joint = jointname

    for file in os.listdir(folder):
        if joint in file:
            if 'angle_mean' in file:
                if 'flex' in file:
                    subtitle = 'Flex./Ext.'
                    # if joint == 'Ankle':
                    #     subtitle = '1st plane'
                    i = 0
                elif 'rot' in file:
                    subtitle = 'Rotation'
                    # if joint == 'Ankle':
                    #     subtitle = '2nd plane'
                    i = 1
                elif 'var' in file:
                    subtitle = 'Var./Valg.'
                    # if joint == 'Ankle':
                    #     subtitle = '3rd plane'
                    i = 2
                elif 'footprog' in file:
                    subtitle = 'Foot Prog.'
                    if joint == 'Ankle':
                        subtitle = 'Foot Prog.'
                    i = 2
                print(file, i)
                df = pd.read_csv(os.path.join(folder, file))
                if 'Left' in file:
                    axs[i, 0].plot(df['pct_gait_cycle'], df['meanShifted50pct'])
                    axs[i, 0].set_title("Left {} ".format(joint) + subtitle)
                    axs[i, 0].grid(color='#95D2F7', linestyle='--', linewidth=0.5)
                elif 'Right' in file:
                    axs[i, 1].plot(df['pct_gait_cycle'], df['Mean'])
                    axs[i, 1].set_title("Right {} ".format(joint) + subtitle)
                    axs[i, 1].grid(color='#95D2F7', linestyle='--', linewidth=0.5)

    for ax in axs.flat:
        ax.set_ylabel('Angle(deg)', color='#BF0F2F')
        ax.set_xlabel('%pct gait cycle', color='#BF0F2F')

    # for ax in axs.flat:
    #     ax.label_outer()

    # plt.subplots_adjust(wspace=0.5, hspace=0.5)
    fig.suptitle('3d angles for {}s'.format(joint))
    # plt.title("{} angles".format(joint))
    plt.savefig(dest_dir + "\\" + "{} angles".format(joint), bbox_inches='tight')
    plt.show(block=True)

def gait_cycle_mean_tester(subfolder, datenow, foldername):
    # files = []
    # for folder in os.listdir("DataFolder\\Testing\\2021-12-02"):
    #     files.append(folder.split("_")[1])
    # column = input("Enter column name\n")
    # joint = input("Enter joint\n")
    # for folder in os.listdir("DataFolder\\Testing\\2021-12-02"):

    # column = input("Enter column name\n")
    # joint = input("Enter joint\n")
    # date = input("Enter date of trial in the format yyyy-mm-dd")
    # read_file = input("Enter file to be used \n")

    joint = subfolder
    date = datenow
    read_file = foldername
    df = pd.read_csv("DataFolder\\" + joint + '\\' + date + '\\' + read_file + '\\' + read_file + '.csv')
    # df = pd.read_csv("DataFolder\\"+joint+ '\\' +read_file+ '\\' +'Raafay_1_gait_cycle.csv')
    print("++++++", df.loc[df['alt_gait_cycle'] == 1].index[0])
    # df.drop(df.index[range(df.loc[df['alt_gait_cycle']==1].index[0])], inplace=True)
    df.index = range(0, len(df))
    df['alt_gait_cycle'] = df['alt_gait_cycle'].round(3)

    gait_cycle = df['alt_gait_cycle']
    # knee_angle = df[column]
    gait_reference = df['hs']
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(date), '{}'.format(read_file))
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass  # already exists

        # numberOfJoints = int(input("Enter no. of Joints"))
    # columns = ['RightKneeflex_angle', 'RightKneevar_angle', 'RightKneerot_angle', 'LeftKneeflex_angle', 'LeftKneevar_angle', 'LeftKneerot_angle',
    #            'RightAnkleflex_angle', 'RightAnkleabd_angle', 'RightAnklerot_angle', 'LeftAnkleflex_angle', 'LeftAnkleabd_angle', 'LeftAnklerot_angle']
    # labels = {'RightKneeflex_angle':'(Right Knee) Flexion-Extension', 'RightKneevar_angle':'(Right Knee) Valgus-Varus', 'RightKneerot_angle':'(Right Knee) Rotation',
    #           'LeftKneeflex_angle':'(Left Knee) Flexion-Extension', 'LeftKneevar_angle':'(Left Knee) Valgus-Varus', 'LeftKneerot_angle':'(Left Knee) Rotation',
    #           'RightAnkleflex_angle': '(Right Ankle) Flexion-Extension', 'RightAnkleabd_angle': '(Right Ankle) Valgus-Varus', 'RightAnklerot_angle': '(Right Ankle) Rotation',
    #           'LeftAnkleflex_angle': '(Left Ankle) Flexion-Extension', 'LeftAnkleabd_angle': '(Left Ankle) Abduction', 'LeftAnklerot_angle': '(Left Ankle) Rotation'}

    columns = [x for x in df.columns if '_angle' in x]
    print(columns)
    all_labels = {'RightKneeflex_angle': '(Right Knee) Flexion-Extension',
                  'RightKneevar_angle': '(Right Knee) Valgus-Varus', 'RightKneerot_angle': '(Right Knee) Rotation',
                  'LeftKneeflex_angle': '(Left Knee) Flexion-Extension',
                  'LeftKneevar_angle': '(Left Knee) Valgus-Varus', 'LeftKneerot_angle': '(Left Knee) Rotation',
                  'RightAnkleflex_angle': '(Right Ankle) Flexion-Extension',
                  'RightAnklefootprog_angle': '(Right Ankle) Foot Prog.', 'RightAnklerot_angle': '(Right Ankle) Rotation',
                  'LeftAnkleflex_angle': '(Left Ankle) Flexion-Extension',
                  'LeftAnklefootprog_angle': '(Left Ankle)  Foot Prog.', 'LeftAnklerot_angle': '(Left Ankle) Rotation',
                  'Rightflex_angle': '(Right) Flexion-Extension', 'Rightvar_angle': '(Right) Valgus-Varus',
                  'Rightrot_angle': '(Right) Rotation',
                  'Leftflex_angle': '(Left) Flexion-Extension', 'Leftvar_angle': '(Left) Valgus-Varus',
                  'Leftrot_angle': '(Left) Rotation',
                  'flex_angle': 'Flexion_Extension', 'var_angle': 'Valgus_Varus', 'rot_angle': 'Rotation'}
    labels = {x: all_labels[x] for x in columns}

    for column in columns:
        print(column)
        try:
            os.makedirs(os.path.join(dest_dir, column))
        except OSError:
            pass  # already exists
        knee_angle = df[column]
        TimeAligned, RolledAvg, ShiftedRolledAvg = pctDelay(knee_angle, column, gait_cycle, gait_reference,
                                                                  dest_dir)
        fig = plt.figure(figsize=(19.2, 10.8))
        if 'Right' in column:
            plt.plot(list(TimeAligned.keys()), RolledAvg, label='{}{}'.format(joint, labels[column]))
        elif 'Left' in column:
            plt.plot(list(TimeAligned.keys()), ShiftedRolledAvg, label='Knee{}'.format(labels[column]))
        # plt.plot(list(TimeAligned.keys()), RolledAvg, label='{}{}'.format(joint, labels[column]))
        plt.title('{} {}'.format(joint, labels[column]))
        plt.savefig(dest_dir + "\\{} {}".format(joint, labels[column]), bbox_inches='tight')
        plt.legend()
        plt.show()
        plt.close()

    plt_averages("DataFolder", joint, date, read_file, "Knee", dest_dir)
    plt_averages("DataFolder", joint, date, read_file, "Ankle", dest_dir)
