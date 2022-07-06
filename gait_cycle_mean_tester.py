# third file in earlier method(to get average plots of all angles/ gait cycles)

import pandas as pd
import os
import matplotlib.pyplot as plt
import utils_sensor_data as utils

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

joint = "Lower_body"
date = "2022-04-12"
read_file = "Test_5_gait_cycle"
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
all_labels = {'RightKneeflex_angle': '(Right Knee) Flexion-Extension', 'RightKneevar_angle': '(Right Knee) Valgus-Varus', 'RightKneerot_angle': '(Right Knee) Rotation',
              'LeftKneeflex_angle': '(Left Knee) Flexion-Extension', 'LeftKneevar_angle': '(Left Knee) Valgus-Varus', 'LeftKneerot_angle': '(Left Knee) Rotation',
              'RightAnkleflex_angle': '(Right Ankle) Flexion-Extension', 'RightAnkleabd_angle': '(Right Ankle) Valgus-Varus', 'RightAnklerot_angle': '(Right Ankle) Rotation',
              'LeftAnkleflex_angle': '(Left Ankle) Flexion-Extension', 'LeftAnkleabd_angle': '(Left Ankle) Abduction', 'LeftAnklerot_angle': '(Left Ankle) Rotation',
              'Rightflex_angle': '(Right) Flexion-Extension', 'Rightvar_angle': '(Right) Valgus-Varus', 'Rightrot_angle': '(Right) Rotation',
              'Leftflex_angle': '(Left) Flexion-Extension', 'Leftvar_angle': '(Left) Valgus-Varus', 'Leftrot_angle': '(Left) Rotation',
              'flex_angle': 'Flexion_Extension', 'var_angle': 'Valgus_Varus', 'rot_angle': 'Rotation'}
labels = {x: all_labels[x] for x in columns}

for column in columns:
    print(column)
    try:
        os.makedirs(os.path.join(dest_dir, column))
    except OSError:
        pass  # already exists
    knee_angle = df[column]
    TimeAligned, RolledAvg, ShiftedRolledAvg = utils.pctDelay(knee_angle, column, gait_cycle, gait_reference, dest_dir)
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

utils.plt_averages("DataFolder", joint, date, read_file, "Knee")
utils.plt_averages("DataFolder", joint, date, read_file, "Ankle")
