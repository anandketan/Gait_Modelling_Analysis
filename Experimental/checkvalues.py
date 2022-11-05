from os import name
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt

# df = pd.read_csv(r'C:\Users\Testing\Fauzan1-02-03-20.csv')
# x=df.values
# min_max = preprocessing.MinMaxScaler()
# x_scaled = min_max.fit_transform(x)
# # df = pd.Dataframe(data=x_scaled[1:,1:], index=x_scaled[1:,0], columns=x_scaled[0,1:])
# df = pd.DataFrame.from_records(x_scaled)

# plt.plot(df.iloc[-200:,44], color = "red", label = "roll")
# plt.plot(df.iloc[-200:,45], color = "green", label = "yaw")
# plt.plot(df.iloc[-200:,46], color = "blue", label = "pitch")
# plt.plot(df.iloc[-200:,47], color = "orange", label = "pressure")

df = pd.read_csv("C:\\Users\\Testing\\Downloads\\position3d.csv")
df.drop(columns = ['Unnamed: 0'], inplace = True)

# df['Xdif'] = df['Left_ankleX'] - df['Left_ankleX'].min()
# df['Ydif'] = df['Left_ankleY'] - df['Left_ankleY'].min()
# df['Zdif'] = df['Left_ankleZ'] - df['Left_ankleZ'].min()

for i in df.columns:
    df['{}dif'.format(i)] = df[i] - df[i].mean()

for i in df.columns[-54:][2::3][8:14][:3]:
    plt.plot(df.loc[1150:1200,i], label = i)
    # plt.plot(df[i], label = i)

# plt.plot(df.loc[1000:1200,'Xdif'], color = "red", label = "X")
# plt.plot(df.loc[1000:1200,'Ydif'], color = "green", label = "Y")
# plt.plot(df.loc[1000:1200,'Zdif'], color = "blue", label = "Z")

plt.legend()
plt.title('Right Lower joints normalized with mean')
plt.show()

for i in df.columns[-54:][2::3][8:14][3:]:
    plt.plot(df.loc[1150:1200,i], label = i)

plt.legend()
plt.title('Left Lower joints normalized with mean')
plt.show()

for i in df.columns[0:54][2::3][8:14]:
    plt.scatter(df[i].std(),df[i].mean(), label = i)

plt.legend()
plt.title('Mean vs Standard Deviation')
plt.show()

for i in df.columns[0:54][2::3][8:14]:
    plt.hist(df[i], bins=72)
    plt.axvline(df[i].mean(), color='blue', linestyle='dashed', linewidth=1, label='Mean')
    plt.axvline(df[i].median(), color='red', linestyle='dashed', linewidth=1, label='Median')
    plt.legend()
    plt.title(i)
    plt.show()