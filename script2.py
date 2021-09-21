import pandas as pd
import datetime
df = pd.DataFrame(columns = ['Time_2'])
i = 0
while (i<30000):
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    df = df.append({'Time_2':ts},ignore_index=True)
    print(i)
    i = i+1

df.to_csv ('/home/kathir/Desktop/Data/script2.csv', index = False, header=True)