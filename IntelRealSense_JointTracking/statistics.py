import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('position3d.csv')
sns.distplot(df['Right_shoulderZ'])
plt.show()

#df1 = df.describe()

#df1.to_csv('position3d_stats.csv')