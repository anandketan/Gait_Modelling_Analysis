import os
import pandas as pd
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))


i = 0
date = ['2022-03-29', '2022-03-30', '2022-03-31']
for day in date:
    dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}'.format(day))
    for folder in os.listdir(dest_dir):
        if '.csv' not in folder and '.png' not in folder:
            df = pd.DataFrame()
            df2 = pd.DataFrame()
            flag = 0
            i += 1
            for file in os.listdir(os.path.join(dest_dir, folder)):
                if 'corrected' in file:
                    print(file)
                    df2 = pd.read_csv(os.path.join(dest_dir, folder, file))
                    plt.plot(df2['_NRollQ'], label='Old-N-Roll')
                    plt.plot(df2['New_NRollQ'], label='New-N-Roll')
                    plt.legend()
                    plt.title(file)
                    plt.show()
                    plt.plot(df2['_CRollQ'], label='Old-C-Roll')
                    plt.plot(df2['New_CRollQ'], label='New-C-Roll')
                    plt.title(file)
                    plt.legend()
                    plt.show()