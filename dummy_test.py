# preetham

import pandas as pd
import numpy as np
import math

for n in range(1,11,1):
    print(n)
    df = pd.read_csv(r'D:\SystemModelling_GaitAnalysis\Reference_data\Shoulder\2022-06-10\angles_Zero_Reference_{}.csv'.format(n))
    h = 'sample_limit'

    df['Ps3prev'] = df[h].shift(1)  # 'Ps3' to be changed to column name of pressure sensor data in csv
    df = df.loc[(df[h] >= 100) & (df['Ps3prev'] < 100)][['Roll', 'Roll_corrected', 'Pitch', 'Yaw', 'Yaw_corrected',
              'Roll-ref', 'Roll_corrected-ref', 'Pitch-ref', 'Yaw-ref', 'Yaw_corrected-ref',
              'Acc_grav_X', 'Acc_grav_Y', 'Acc_grav_Z', 'sample_limit']]
    df.index = np.arange(1, len(df)+1)
    df.index.name = 'Position#'
    print(df)
    df.to_csv('10strapping_{}.csv'.format(n))
