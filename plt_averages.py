import matplotlib.pyplot as plt
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
cycle = 0
joint = 'Test'
date = '2022-05-13'
# read_file = 'Test_8_gait_cycle\\cycle_{}'.format(cycle)
read_file = 'Test_8_gait_cycle'
dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(date), '{}'.format(read_file))


def plt_averages(mainfolder, subfolder, date, foldername, jointname, dest_dir):
    folder = os.path.join(mainfolder, subfolder, date, foldername)
    index = [1, 3, 5, 2, 4, 6]
    i = 0

    fig = plt.figure(figsize=(19.2, 10.8))
    # gs = fig.add_gridspec(3, 2, wspace=0.04)
    gs = fig.add_gridspec(3, 2, wspace=0.13, hspace=0.33)
    # axs = gs.subplots(sharex=True, sharey='row')
    axs = gs.subplots()
    # fig.suptitle("3d angles for both knees")
    joint = jointname

    for file in os.listdir(folder):
        if joint in file:
            if 'angle_mean' in file:
                if 'flex' in file:
                    subtitle = 'Flex./Ext.'
                    # if joint == 'Ankle':
                    #     subtitle = '1st plane'
                    i = 0
                elif 'rot' in file:
                    subtitle = 'Rotation'
                    # if joint == 'Ankle':
                    #     subtitle = '2nd plane'
                    i = 1
                elif 'var' in file:
                    subtitle = 'Var./Valg.'
                    # if joint == 'Ankle':
                    #     subtitle = '3rd plane'
                    i = 2
                elif 'footprog' in file:
                    subtitle = 'Foot Prog.'
                    if joint == 'Ankle':
                        subtitle = 'Foot Prog.'
                    i = 2
                print(file, i)
                df = pd.read_csv(os.path.join(folder, file))
                if 'Left' in file:
                    axs[i, 0].plot(df['pct_gait_cycle'], df['meanShifted50pct'])
                    axs[i, 0].set_title("Left {} ".format(joint) + subtitle)
                    axs[i, 0].grid(color='#95D2F7', linestyle='--', linewidth=0.5)
                elif 'Right' in file:
                    axs[i, 1].plot(df['pct_gait_cycle'], df['Mean'])
                    axs[i, 1].set_title("Right {} ".format(joint) + subtitle)
                    axs[i, 1].grid(color='#95D2F7', linestyle='--', linewidth=0.5)

    for ax in axs.flat:
        ax.set_ylabel('Angle(deg)', color='#BF0F2F')
        ax.set_xlabel('%pct gait cycle', color='#BF0F2F')

    # for ax in axs.flat:
    #     ax.label_outer()

    # plt.subplots_adjust(wspace=0.5, hspace=0.5)
    fig.suptitle('3d angles for {}s'.format(joint))
    # plt.title("{} angles".format(joint))
    plt.savefig(dest_dir + "\\" + "{} angles".format(joint), bbox_inches='tight')
    plt.show(block=True)


print(dest_dir)
plt_averages("DataFolder", joint, date, read_file, "Ankle", dest_dir)
for file in os.listdir(dest_dir):
    if 'cycle_' in file:
        print(file)
        plt_averages("DataFolder", joint, date, read_file+"\\{}".format(file), "Ankle", dest_dir+"\\{}".format(file))

