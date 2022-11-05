import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv(r'C:\Users\Testing\Desktop\Biomechanics_Gait_Analysis\DataFolder\2021-09-16_12_30_36\right_ankle_sensorG.csv')[1000:]
df.index = range(0,len(df))

def shift_down():
    a=0
    df['Yawnewnew'] = [0.0]*len(df)
    for i in range(len(df[' Yaw'])-1):
        df['Yawnewnew'][i] = df[' Yaw'][i] + a
        if(df[' Yaw'][i]-df[' Yaw'][i+1]>=300):
            # a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
            a=0
        elif(df[' Yaw'][i]-df[' Yaw'][i+1]>=30):
            a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
        elif(df[' Yaw'][i]-df[' Yaw'][i+1]<=-30):
            # a=0
            a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
    #     df['Yawnewnew'][i] = df['Yawnew'][i] + a
    df['Yawnewnew'][-1:] = df[' Yaw'][-1:] + a
    shift = df['Yawnewnew'][0] - df[' Yaw'][0]
    plt.plot(df[' Yaw'][:], '*-', label="Yaw")
    plt.plot(df['Yawnewnew'][:],label="Yawnew")

    plt.legend()
    plt.show()


def shift_up():
    a=0
    df['Yawnewnew'] = [0.0]*len(df)
    for i in range(len(df[' Yaw'])-1):
        df['Yawnewnew'][i] = df[' Yaw'][i] + a
        if(df[' Yaw'][i]-df[' Yaw'][i+1]>=70):
            a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
            # a=0
        elif(df[' Yaw'][i]-df[' Yaw'][i+1]<=-70):
            a=0
            # a=df['Yawnewnew'][i]-df[' Yaw'][i+1]
    #     df['Yawnewnew'][i] = df['Yawnew'][i] + a
    df['Yawnewnew'][-1:] = df[' Yaw'][-1:] + a
    shift = df['Yawnewnew'][0] - df[' Yaw'][0]
    plt.plot(df[' Yaw'][:],label="Yaw")
    plt.plot(df['Yawnewnew'][:],label="Yawnew")

    plt.legend()
    plt.show()

if abs(df['Pitch'][0]-360)>abs(df[' Yaw'][0]):
    shift_down()
else:
    shift_up()
