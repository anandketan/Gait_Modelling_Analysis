import os
import pandas as pd
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))

with open('statsChitradurgaTest', 'w') as file1:
    file1.write('No.,Name,Gender,Age,Height(cm),Weight(Kg),Trial,'
                'Initial Angle(deg),Actual Left(deg),Max Left(deg),Actual Right(deg),Max Right(deg),Range(deg),Score\n')
    i = 0
    date = ['2022-02-10', '2022-02-11']
    for day in date:
        dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}'.format(day))
        for folder in os.listdir(dest_dir):
            if '.csv' not in folder:
                i += 1
                for file in os.listdir(os.path.join(dest_dir, folder)):
                    if 'allGameSensorData' in file:
                        print(i, "--->", file, "....*", folder.split('_')[0], "..", folder.split('_')[1])
                        df = pd.read_csv(os.path.join(dest_dir, folder, file))
                        file1.write(str(i) + ',' + str(folder.split('_')[0]) + ',' + str(0) + ',' + str(0) + ',' + str(
                            0) + ',' + str(0) + ',' + str(folder.split('_')[1]) + ',' + str(
                            df['_GPitchQ'][:100].mean()) + ',' + str(0) + ',' + str(
                            df['_GPitchQ'].min()) + ',' + str(0) + ',' + str(df['_GPitchQ'].max()) + ',' + str(
                            df['_GPitchQ'].max() - df['_GPitchQ'].min()) + ',' + str(0) + '\n')
                        plt.plot(df['time'] - df['time'][0], df['_GPitchQ'])
                        plt.legend()
                        plt.title(folder)
                        plt.savefig(os.path.join(dest_dir, folder), bbox_inches='tight')
                        plt.show(block=False)
                        plt.pause(0.005)
                        plt.close()
