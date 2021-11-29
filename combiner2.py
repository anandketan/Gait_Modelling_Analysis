import os
import pandas as pd
import matplotlib.pyplot as plt

cycle = []
data = []
joint = "right_knee"
date = "2021-11-23"
read_file = "Nikhil_{}_gait_cycle".format(6)
df = pd.read_csv("DataFolder\\"+joint + '\\'+date + '\\' +read_file+ '\\' +read_file+'.csv')
df = df.loc[df['alt_gait_cycle']<=3]
# print(len(Gait_Cycle1))
plt.plot(df['alt_gait_cycle'],df['flex_angle'])
# plt.plot([df['Mean'].iloc[0]]*101, '--')


plt.title("Flexion/Extension Right Knee")
plt.legend()
plt.show()
