import matplotlib.pyplot as plt
import pandas as pd
import os

folder = os.path.join("DataFolder", "Knees", "2022-01-07", "Test_1_gait_cycle")
index = [1, 3, 5, 2, 4, 6]
i = 0

fig = plt.figure()
gs = fig.add_gridspec(3, 2, wspace=0.04)
axs = gs.subplots(sharex=True, sharey='row')
# axs = gs.subplots()
# fig.suptitle("3d angles for both knees")
joint = "Knee"

for file in os.listdir(folder):
    if joint in file:
        if 'angle_mean' in file:
            if 'flex' in file:
                subtitle = 'Flex./Ext.'
                i = 0
            elif 'rot' in file:
                subtitle = 'Rotation'
                i = 1
            elif 'var' in file:
                subtitle = 'Var./Valg.'
                i = 2
            elif 'abd' in file:
                subtitle = 'Abd./Add.'
                i = 2
            print(file, i)
            df = pd.read_csv(os.path.join(folder, file))
            if 'Left' in file:
                axs[i, 0].plot(df['pct_gait_cycle'], df['meanShifted50pct'])
                axs[i, 0].set_title("Left {} ".format(joint)+subtitle)
                axs[i, 0].grid(color='#95D2F7', linestyle='--', linewidth=0.5)
            elif 'Right' in file:
                axs[i, 1].plot(df['pct_gait_cycle'], df['Mean'])
                axs[i, 1].set_title("Right {} ".format(joint)+subtitle)
                axs[i, 1].grid(color='#95D2F7', linestyle='--', linewidth=0.5)

for ax in axs.flat:
    ax.set_ylabel('Angle(deg)', color='#BF0F2F')
    ax.set_xlabel('%pct gait cycle', color='#BF0F2F')

for ax in axs.flat:
    ax.label_outer()

# plt.subplots_adjust(wspace=0.5, hspace=0.5)
fig.suptitle('3d angles for {}s'.format(joint))
plt.show()
