# plot gait cycles

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import floor

df = pd.read_csv('Fauzan1-02-03-20-with_gait_cycle.csv')

gait_cycle = df['alt_gait_cycle']
knee_angle = df['Pitch3']
# plt.plot(gait_cycle % 1,knee_angle)
# plt.show()

n = 0#nth cycle

temp = []
data = []#all angle data

rate = []
cycles = []#all cycles

for i in range(gait_cycle.shape[0]):
    if(gait_cycle[i].is_integer()):
        n = int(gait_cycle[i])
        if rate:
            cycles.append(rate)
            data.append(temp)
            # rate.clear()
            rate = []
            temp = []
        else:
            rate.append((gait_cycle[i] - n)*100)
            temp.append(knee_angle[i])
    else:
        rate.append((gait_cycle[i]-n)*100)
        temp.append(knee_angle[i])
if rate:
    cycles.append(rate)
    data.append(temp)
# print(cycles)
# print(data)

for j in range(len(cycles)):
    plt.plot(cycles[j][:], data[j][:], alpha=0.6, color='#4287f5')

plt.xlabel('Gait cycle(%)')
plt.ylabel('Degrees')
plt.title('Knee flexion and abduction')
plt.show()