#delete any file

import os

script_dir = os.path.dirname(os.path.abspath(__file__))

date = ['2022-02-10', '2022-02-11']
i=0
for day in date:
    dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}'.format(day))
    for folder in os.listdir(dest_dir):
        if '.csv' not in folder and '.png' not in folder:
        # try:
            os.listdir(os.path.join(dest_dir, folder))
            i += 1
            for file in os.listdir(os.path.join(dest_dir, folder)):
                if 'new' in file:
                    print(i, file)
                    os.remove(os.path.join(dest_dir, folder, file))
