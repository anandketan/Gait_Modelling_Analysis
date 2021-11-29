import os
import pandas as pd
import matplotlib.pyplot as plt

cycle = []
data = []
for folder in os.listdir("DataFolder\\StaticOnBox\\2021-11-26"):
    # print(folder.split("_")[1])
    df = pd.read_csv("DataFolder\\StaticOnBox\\2021-11-26\\"+folder+"\\var_angleStaticOnBox_mean_std.csv")
    Mean1 = df['Mean']
    print(df['Mean'].iloc[0], df['Mean'].iloc[-1])
    # Mean1 = df['Mean'] - df['Mean'][0]
    data.append(Mean1)
    Gait_Cycle1 = df['pct_gait_cycle']
    cycle.append(Gait_Cycle1)
    # print(len(Gait_Cycle1))
    plt.plot(Gait_Cycle1, Mean1, alpha=1)
    # plt.plot([df['Mean'].iloc[0]]*101, '--')

dict_comb = dict()
for cyc, dat in zip(cycle, data):
    for i, j in zip(cyc, dat):
        if i in dict_comb.keys():
            dict_comb[i].append(j)
        else:
            dict_comb[i] = [j]
time_aligned = pd.DataFrame.from_dict(dict_comb, orient='index').transpose()

# plt.plot(time_aligned.columns, time_aligned.mean(),label='Mean')
# plt.fill_between(time_aligned.columns, time_aligned.mean()-time_aligned.std(), time_aligned.mean()+time_aligned.std(), alpha=1, color='black', facecolor='lightgrey',label='Standard deviation')

plt.xlabel("% Gait Cycle")
plt.ylabel("Degrees")
plt.title("Varus Valgus Static")
plt.legend()
plt.show()
