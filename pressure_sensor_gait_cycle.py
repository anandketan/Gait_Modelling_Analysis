import numpy as np
import pandas as pd

df = pd.read_csv(r'C:\Users\Testing\Fauzan1-02-03-20.csv') #replace with path to any csv with pressure sensor data

df['Ps3prev'] = df['Ps3'].shift(1) #'Ps3' to be changed to column name of pressure sensor data in csv
df['Gait_cycle'] = [0]*len(df)
df['Gait_cycle'] = (df['Ps3'] == 4095) & (df['Ps3prev'] < 4095)
df['Gait_cycle'].replace([np.nan, False, True],[0, 0, 1],inplace=True)
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

df = df.drop(range(0,df.loc[df['Gait_cycle']==1].index[0])) #drops everything before the start of the first cycle

df['alt_gait_cycle'] = df['Gait_cycle'] - 1 #starts cycle numbering from 0 instead of 1

df.to_csv(r'C:\Users\Testing\Fauzan1-02-03-20-with_gait_cycle.csv') #destination path 