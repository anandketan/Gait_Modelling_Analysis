import pandas as pd
df1 = pd.read_csv('/home/kathir/Desktop/Data/script1.csv')
df2 = pd.read_csv('/home/kathir/Desktop/Data/script2.csv')
df3 = pd.DataFrame(columns = ['Difference'])
df3['Difference'] = df2['Time_2']-df1['Time_1']
print(df1.describe())
print(df2.describe())
print(df3.describe())