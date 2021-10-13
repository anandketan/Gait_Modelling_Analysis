import numpy as np
import pandas as pd

dest_path = input("Enter destination path \n")

df = pd.read_csv(r'C:\Users\Testing\Desktop\Biomechanics_Gait_Analysis\datanewfauzanrightankle1633937368.782519.csv')[:45000] #replace with path to any csv with pressure sensor data
df.index = range(0,len(df))

# df['yaw_new'] = df[' Yaw'] - df[' Yaw'].mean()
# df['roll_new'] = df['Roll'] - df['Roll'].mean()
# df['pitch_new'] = df['Pitch'] - df['Pitch'].mean()
# df['Knee_angle'] = df['3Pitch'] - df['2Pitch']
# df['Knee_angle2'] = df['3Roll'] - df['2Roll']
# df['Knee_angle3'] = df['3Yaw'] - df['2Yaw']

# def shift_down():
#     a=0
#     df['Yawnewnew'] = [0.0]*len(df)
#     for i in range(len(df[' Yaw'])-1):
#         df['Yawnewnew'][i] = df[' Yaw'][i] + a
#         if(df[' Yaw'][i]-df[' Yaw'][i+1]>=300):
#             # a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
#             a=0
#         elif(df[' Yaw'][i]-df[' Yaw'][i+1]>=70):
#             a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
#         elif(df[' Yaw'][i]-df[' Yaw'][i+1]<=-70):
#             # a=0
#             a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
#     #     df['Yawnewnew'][i] = df['Yawnew'][i] + a
#     df['Yawnewnew'][-1:] = df[' Yaw'][-1:] + a


# def shift_up():
#     a=0
#     df['Yawnewnew'] = [0.0]*len(df)
#     for i in range(len(df[' Yaw'])-1):
#         df['Yawnewnew'][i] = df[' Yaw'][i] + a
#         if(df[' Yaw'][i]-df[' Yaw'][i+1]>=70):
#             a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
#             # a=0
#         elif(df[' Yaw'][i]-df[' Yaw'][i+1]<=-70):
#             a=0
#             # a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
#     #     df['Yawnewnew'][i] = df['Yawnew'][i] + a
#     df['Yawnewnew'][-1:] = df[' Yaw'][-1:] + a

# if abs(df[' Yaw'][0]-360)>abs(df[' Yaw'][0]):
#     shift_down()
# else:
#     shift_up()

df['Ps3prev'] = df['hs'].shift(1) #'Ps3' to be changed to column name of pressure sensor data in csv
df['Gait_cycle'] = [0]*len(df)
df['Gait_cycle'] = (df['hs'] >= 100) & (df['Ps3prev'] < 100)
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

print(df.index)
df = df.drop(range(0,df.loc[df['Gait_cycle']==1].index[0])) #drops everything before the start of the first cycle

df['alt_gait_cycle'] = df['Gait_cycle'] - 1 #starts cycle numbering from 0 instead of 1

df.to_csv(dest_path+'.csv') #destination path 