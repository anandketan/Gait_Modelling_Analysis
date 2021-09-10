##simple reach out annotation with 2d angles

import numpy as np
import pandas as pd

df = pd.read_csv(r'diff_reachout_position3d.csv') 

df['Angle2dprev'] = df['Angle2d'].shift(1) 
df['reachout_start'] = [0]*len(df)
df['reachout_start'] = (df['Angle2d'] >75) & (df['Angle2dprev'] <= 75)
df['reachout_start'].replace([np.nan, False, True],[0, 0, 1],inplace=True)
df['reachout_end'] = [0]*len(df)
df['reachout_end'] = (df['Angle2d'] <=75) & (df['Angle2dprev'] >75)
df['reachout_end'].replace([np.nan, False, True],[0, 0, 1],inplace=True)

df.to_csv(r'reachout.csv') #destination path
# print(df['reachout'].value_counts())
