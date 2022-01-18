import numpy as np
import pandas as pd
import os

def add_gait_cycle(dest_path = "", read_path = "",joint = "",hstype=1):

    if dest_path == "":
        dest_path = input("Enter destination path with .csv extension\n")

    if read_path == "":
        read_path = input("Enter read path without using .csv extension\n")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}.csv'.format(read_path))

    df = pd.read_csv(read_path)[:] #replace with path to any csv with pressure sensor data
    df.index = range(0,len(df))

    if hstype:
        h = 'hs'
    else:
        h = 'hs_US'


    df['Ps3prev'] = df[h].shift(1) #'Ps3' to be changed to column name of pressure sensor data in csv
    df['Gait_cycle'] = [0]*len(df)
    df['Gait_cycle'] = (df[h] >= 100) & (df['Ps3prev'] < 100)
    df['Gait_cycle'].replace([np.nan, False, True],[0, 0, 1],inplace=True)
    last = df.loc[df['Gait_cycle']==1].index
    df.loc[df['Gait_cycle']==1, 'Gait_cycle'] = np.arange(1,df['Gait_cycle'].value_counts()[1]+1,1)

    starts = df.loc[df['Gait_cycle']!=0]

    for i in starts['Gait_cycle'][:-1]:
        x = 1/((df.loc[df['Gait_cycle']==(i+1)].index - df.loc[df['Gait_cycle']==i].index)[0])
        fill = np.linspace(i+x,i+1-x, (df.loc[df['Gait_cycle']==(i+1)].index - df.loc[df['Gait_cycle']==i].index)[0]-1)
        df.loc[df.loc[df['Gait_cycle']==i].index[0]+1:df.loc[df['Gait_cycle']==(i+1)].index[0]-1, 'Gait_cycle'] = fill

    n = starts['Gait_cycle'][-1:].values[0]
    i = starts['Gait_cycle'][-1:].index[0]
    j = df.iloc[-1].name

    fill = np.linspace(n+x,n+(j-i)*x, j-i) #last cycle filled with steps from previous cycle since it is not complete

    df.loc[i+1:j, 'Gait_cycle'] = fill

    print(df.index)
    print(last[-1])
    df = df.loc[:last[-1]]
    df = df.drop(range(0,df.loc[df['Gait_cycle']==1].index[0])) #drops everything before the start of the first cycle

    df['alt_gait_cycle'] = df['Gait_cycle'] - 1 #starts cycle numbering from 0 instead of 1

    df.to_csv(dest_path) #destination path

    return dest_path

# dest_path = add_gait_cycle(r'C:\Users\Admin\Desktop\SystemModelling_GaitAnalysis\DataFolder\Testing\2021-12-03\test_1_gait_cycle\test_1_gait_cycle.csv', r'C:\Users\Admin\Desktop\SystemModelling_GaitAnalysis\DataFolder\Testing\2021-12-03\test_1_gait_cycle\diff_pitch_test_1.csv', "Testing")