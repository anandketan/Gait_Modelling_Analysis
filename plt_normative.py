import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import floor
import time
from scipy.stats import circmean
from scipy.stats import circstd
from collections import deque
import os
import subprocess
import glob


df_norm = pd.read_csv('HipFlexExt.csv')
# print(df_norm)
Mean = df_norm['Mean']
Gait_Cycle = df_norm['% Gait Cycle']
Std_D = df_norm['SD']

plt.plot(Gait_Cycle,Mean,color='navy',label='Normative mean')
plt.fill_between(Gait_Cycle, Mean-Std_D, Mean+Std_D, alpha=1, color='lightgrey', facecolor='lavender',label='Normative Standard deviation')
plt.show()