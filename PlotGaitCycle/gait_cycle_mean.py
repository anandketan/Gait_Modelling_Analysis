import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import floor
import time
from scipy.stats import circmean
from scipy.stats import circstd


def rolling_avg(a,alist,window_size):
    l = int(window_size/2)
    print(l)
    before = alist[0]
    after = alist[-1]
    alist = [before]*(l-1) + alist + [after]*l
    rolled_avg = [0]*len(a)
    j=0
    for i,n in enumerate(alist):
        if i>=(l-1) and i<len(alist)-l:
            rolled_avg[j] = sum(alist[i-l+1:i+l+1])/window_size
            # rolled_avg[j] = circmean(alist[i-l+1:i+l+1], high=high, low=low,nan_policy='omit')
            j+=1
    return rolled_avg


column = input("Enter column name\n")
# high = int(input("Enter high"))
# print(high)
# low = int(input("Enter Low"))
# print(low)
read_file = input("Enter file to be used \n")
df = pd.read_csv(read_file+'.csv')
print("++++++",df.loc[df['alt_gait_cycle']==1].index[0])
df.drop(df.index[range(df.loc[df['alt_gait_cycle']==1].index[0])], inplace=True)
df.index = range(0,len(df))
df['alt_gait_cycle'] = df['alt_gait_cycle'].round(3)

gait_cycle = df['alt_gait_cycle']
knee_angle = df[column]
gait_reference = df['hs']

print(len(gait_reference))
print(len(knee_angle))
print(len(gait_cycle))

n = 0#nth cycle
temp = []
data = []#all angle data
rate = []
cycles = []#all cycles
temp_ref = []
value_ref = []

for i in range(gait_cycle.shape[0]):
    if(gait_cycle[i].is_integer()):
        n = int(gait_cycle[i])
        if rate:
            cycles.append(rate)
            data.append(temp)
            value_ref.append(temp_ref)
            rate = []
            temp = []
            temp_ref = []
            rate.append((gait_cycle[i] - n)*100)
            temp.append(knee_angle[i])
            temp_ref.append(gait_reference[i])
        else:
            rate.append((gait_cycle[i] - n)*100)
            temp.append(knee_angle[i])
            temp_ref.append(gait_reference[i])
    else:
        rate.append((gait_cycle[i]-n)*100)
        temp.append(knee_angle[i])
        temp_ref.append(gait_reference[i])

if rate:
    cycles.append(rate)
    data.append(temp)
    value_ref.append(temp_ref)

for i,(cycle,dat) in enumerate(zip(cycles,data)):
    cycles[i] = [round(x,3) for x in cycles[i]]

for i,dat in enumerate(data):
    init = dat[0]
    

dict_comb = dict()
for cycle,dat in zip(cycles,data):
    for i,j in zip(cycle, dat):
        if i in dict_comb.keys():
            dict_comb[i].append(j)
        else:
            dict_comb[i] = [j]

sorted_dictcomb = sorted(dict_comb.items())
timed_dict = dict(sorted_dictcomb)

time_aligned=pd.DataFrame.from_dict(timed_dict,orient='index').transpose()
single_value_columns = [x for x in time_aligned.columns if len(time_aligned[x].unique())==2]

ta=dict(time_aligned.mean())
# ta = {}
# for i in time_aligned.columns:
#     ta[i] = circmean(time_aligned[i], high=high, low = low,nan_policy='omit')

ta_list = list(ta.values())
print(len(ta))
window_size = (len(ta)/10)-(len(ta)/10)%10
print(window_size)
rolled_avg = rolling_avg(ta,ta_list,window_size)

ta_std = time_aligned.std()
# ta_std = {}
# for i in time_aligned.columns:
#     ta_std[i] = circstd(time_aligned[i], high=high, low = low,nan_policy='omit')
# tdiff1list = [0]*len(rolled_avg)
# tdiff2list = [0]*len(rolled_avg)
# for i,(j,k) in enumerate(zip(rolled_avg,ta_std.values())):
#     tdiff1list[i] = j-k
#     tdiff2list[i] = j+k
for i in single_value_columns:
    ta_std[i]=0
ta_diff1 = rolled_avg-ta_std
ta_diff2 = rolled_avg+ta_std
tdiff1list = list(dict(ta_diff1).values())
tdiff2list = list(dict(ta_diff2).values())
# print(tdiff1list)

rolled_avg_tdiff1 = rolling_avg(ta,tdiff1list,window_size)
rolled_avg_tdiff2 = rolling_avg(ta,tdiff2list,window_size)

print(len(value_ref))
print(len(data))
print(len(cycles))

for j in range(len(cycles)):#len(cycles)
    # print(len(data[j]))
    # print(len(value_ref[j]))
    # print(len(cycles[j]))
    plt.plot(cycles[j][:], data[j][:], alpha=0.6, color='#4287f5')
    # plt.plot(cycles[j][:], value_ref[j][:], alpha=0.6, color='green')
    # plt.title(j)
    # plt.show()
plt.plot(list(ta.keys()),rolled_avg,color='red',label='Mean')
# plt.plot(list(ta.keys()),rolled_avg_tdiff1, color='orange')
# plt.plot(list(ta.keys()),rolled_avg_tdiff2, color='green')
plt.fill_between(list(ta.keys()), rolled_avg_tdiff1, rolled_avg_tdiff2, color='grey', label='Standard deviation')
plt.title("Right Knee {}".format(column))
plt.legend()
plt.show()