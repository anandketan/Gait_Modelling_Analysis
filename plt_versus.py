import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy import interpolate
import math
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
cycle = 0
joint = 'Lower_body'
date = '2022-04-13'
# read_file = 'Test_8_gait_cycle\\cycle_{}'.format(cycle)
read_file = ["Fauzan_1_gait_cycle", "Fauzan_2_gait_cycle", "Raafay_1_gait_cycle", "Raafay_2_gait_cycle", "Raafay_4_gait_cycle"]
bimra_file = ['fauzan_trail1.csv', 'fauzan_trail2.csv', 'raafay_trail1.csv', 'raafay_trail2.csv', 'raafay_trail4.csv']
# dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(date), '{}'.format(read_file))
# read_file = ["Raafay_3_gait_cycle"]
# bimra_file = ['raafay_trail3.csv']

# df_b = pd.read_csv(os.path.join(dest_dir, 'raafay_trail3.csv'))

dict = {'Ankle': 'A', 'Knee': 'K'}

def plt_averages(mainfolder, subfolder, date, foldername, jointname, dest_dir, cycle):
    folder = os.path.join(mainfolder, subfolder, date, foldername)
    index = [1, 3, 5, 2, 4, 6]
    i = 0
    rows = 3
    if jointname == 'Knee':
        rows = 3
    elif jointname == 'Ankle':
        rows = 2
    fig = plt.figure(figsize=(19.2, 10.8))
    # gs = fig.add_gridspec(2, 2, wspace=0.04)
    gs = fig.add_gridspec(rows, 2, wspace=0.13, hspace=0.33) #knee
    # axs = gs.subplots(sharex=True, sharey='row')
    axs = gs.subplots()
    # fig.suptitle("3d angles for both knees")
    joint = jointname

    for file in os.listdir(folder):
        if joint in file:
            if 'angle_mean' in file:
                if 'flex' in file:
                    subtitle = 'Flex-Ext'
                    column = dict[joint] + 'FE.M'
                    # if joint == 'Ankle':
                    #     subtitle = '1st plane'
                    i = 0
                elif 'rot' in file:
                    subtitle = 'Rotation'
                    column = dict[joint] + 'IE.M'
                    if joint == 'Ankle':
                        continue
                    i = 1
                elif 'var' in file:
                    subtitle = 'Var-Valg'
                    column = dict[joint] + 'AA.M'
                    # if joint == 'Ankle':
                    #     subtitle = '3rd plane'
                    i = 2
                elif 'footprog' in file:
                    subtitle = 'Foot-Prog'
                    column = dict[joint] + 'IE.M'
                    if joint == 'Ankle':
                        subtitle = 'Foot-Prog'
                    i = 1
                else:
                    subtitle = 'Foot-Progression'
                    column = dict[joint] + 'IE.M'
                    i = 1
                print(file, i)
                df = pd.read_csv(os.path.join(folder, file))
                # fig = plt.figure(figsize=(19.2, 10.8))
                if 'Left' in file:
                    column = ' acmL' + column
                    f = interpolate.interp1d(df_b[' Sample'], df_b[column])
                    xnew = np.linspace(df_b[' Sample'][0], df_b[' Sample'].iloc[-1], 1000)
                    error = [abs(a-b) for a, b in zip(list(f(xnew)), df['meanShifted50pct']+(df_b[column][0]-df['meanShifted50pct'][0])) ]
                    axs[i, 0].plot(df['pct_gait_cycle'], df['meanShifted50pct']+(df_b[column][0]-df['meanShifted50pct'][0]), label='IMU_shifted', color='orange')
                    axs[i, 0].plot(df_b[' Sample'], df_b[column], label='BIMRA')
                    # axs[i, 0].plot(list(xnew), error, label='error')
                    axs[i, 0].set_title("Left {} ".format(joint) + subtitle)
                    axs[i, 0].grid(color='#95D2F7', linestyle='--', linewidth=0.5)
                elif 'Right' in file:
                    column = ' acmR' + column
                    f = interpolate.interp1d(df_b[' Sample'], df_b[column])
                    xnew = np.linspace(df_b[' Sample'][0], df_b[' Sample'].iloc[-1], 1000)
                    error = [abs(a - b) for a, b in
                             zip(list(f(xnew)), df['Mean'] + (df_b[column][0] - df['Mean'][0]))]
                    axs[i, 1].plot(df['pct_gait_cycle'], df['Mean']+(df_b[column][0]-df['Mean'][0]), label='IMU_shifted', color='orange')
                    axs[i, 1].plot(df_b[' Sample'], df_b[column], label = 'BIMRA')
                    # axs[i, 1].plot(list(xnew), error, label='error')
                    axs[i, 1].set_title("Right {} ".format(joint) + subtitle)
                    axs[i, 1].grid(color='#95D2F7', linestyle='--', linewidth=0.5)
                # if 'Left' in file:
                #     column = ' acmL' + column
                #     plt.plot(df['pct_gait_cycle'], df['meanShifted50pct'], label='IMU', alpha=0.4, color='orange')
                #     plt.plot(df['pct_gait_cycle'], df['meanShifted50pct']+(df_b[column][0]-df['meanShifted50pct'][0]), label='IMU_shifted', color='orange')
                #     plt.plot(df_b[' Sample'], df_b[column], label='BIMRA')
                #     plt.title("Left {} ".format(joint) + subtitle + " - " + cycle)
                #     plt.grid(color='#95D2F7', linestyle='--', linewidth=0.5)
                #     plt.legend()
                #     plt.savefig(dest_dir + "\\" + "Left{}{} anglesvsBimra(shifted)".format(joint, subtitle), bbox_inches='tight')
                #     # plt.show(block=True)
                #     plt.show(block=False)
                #     plt.pause(0.005)
                #     plt.close()
                #
                # elif 'Right' in file:
                #     column = ' acmR' + column
                #     plt.plot(df['pct_gait_cycle'], df['Mean'], label='IMU', alpha=0.4, color='orange')
                #     plt.plot(df['pct_gait_cycle'], df['Mean']+(df_b[column][0]-df['Mean'][0]), label='IMU_shifted', color='orange')
                #     plt.plot(df_b[' Sample'], df_b[column], label = 'BIMRA')
                #     plt.title("Right {} ".format(joint) + subtitle + " - " + cycle)
                #     plt.grid(color='#95D2F7', linestyle='--', linewidth=0.5)
                #     plt.legend()
                #     plt.savefig(dest_dir + "\\" + "Right{}{} anglesvsBimra(shifted)".format(joint, subtitle), bbox_inches='tight')
                #     # plt.show(block=True)
                #     plt.show(block=False)
                #     plt.pause(0.005)
                #     plt.close()
                # print(subtitle)


    for ax in axs.flat:
        ax.set_ylabel('Angle(deg)', color='#BF0F2F')
        ax.set_xlabel('%pct gait cycle', color='#BF0F2F')

    # for ax in axs.flat:
    #     ax.label_outer()

    # plt.subplots_adjust(wspace=0.5, hspace=0.5)
    # fig.suptitle('Angles for {}s - {}'.format(joint, cycle))
    fig.suptitle('Angles for {}s - {}'.format(joint, cycle))
    # plt.title("{} angles".format(joint))
    # plt.legend()
    handles, labels = axs[i, 1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper right')
    plt.savefig(dest_dir + "\\" + "{} anglesvsBimra".format(joint), bbox_inches='tight')
    plt.show(block=True)

# fig = plt.figure(figsize=(19.2, 10.8))
for rf, bf in zip(read_file, bimra_file):
    dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(date), '{}'.format(rf))
    df_b = pd.read_csv(os.path.join(dest_dir, bf))
    print(dest_dir)
    plt_averages("DataFolder", joint, date, rf, "Knee", dest_dir, "average of all cycles")
    for file in os.listdir(dest_dir):
        if 'cycle_' in file:
            print(file)
            plt_averages("DataFolder", joint, date, rf+"\\{}".format(file), "Knee", dest_dir+"\\{}".format(file), file)

# for file in os.listdir(dest_dir):
# plt.title("Left {} ".format(joint) + subtitle)
# plt.grid(color='#95D2F7', linestyle='--', linewidth=0.5)
# plt.legend()
# plt.show()

