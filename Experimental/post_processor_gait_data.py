# correction for yaw/picth/roll after collection from raw data of gait

import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import utils_sensor_data as utils

script_dir = os.path.dirname(os.path.abspath(__file__))

axx = 0
ay = 1
az = 2
gx = 3
gy = 4
gz = 5
q1 = 6
q2 = 7
q3 = 8
q4 = 9
calcYaw = 10
calcPitch = 11
calcRoll = 12
Yaw = 13
Pitch = 14
Roll = 15
count_sensor = 16
timer = 17
hs = 18
dist = 19
gravaccx = 20
gravaccy = 21
gravaccz = 22

device_list = ['D', 'C', 'H', 'U', 'G', 'A', 'B']

prevdata = {}
data = {}
d = {}
prevyaw = {}
nyaw = {}
prevroll = {}
nroll = {}
prevpitch = {}
npitch = {}


mainfolder = "DataFolder"
substring = "allSensorData"
i = 0
date = ['2022-04-13']
joint = "Lower_body"
folders = ["Fauzan_1_gait_cycle", "Fauzan_2_gait_cycle", "Raafay_1_gait_cycle", "Raafay_2_gait_cycle", "Raafay_3_gait_cycle", "Raafay_4_gait_cycle"]

for day in date:
    dest_dir = os.path.join(script_dir, mainfolder, joint, '{}'.format(day))
    for folder in os.listdir(dest_dir):
        if folder in folders:
            os.listdir(os.path.join(dest_dir, folder))
            i += 1
            for file in os.listdir(os.path.join(dest_dir, folder)):
                if substring in file:
                    print(i, file)
                    newfile = file.split('_')[0] + file.split('_')[1] + 'corrected.csv'
                    newgaitcycle = file.split('_')[0] + file.split('_')[1] + 'gait_cycle_new.csv'
                    with open(os.path.join(dest_dir, folder, newfile), 'w') as filenew, open(os.path.join(dest_dir, folder, file), 'r') as fileold:
                        filenew.write('_EStep,hs,'
                            '_DYawQ,_DPitchQ,_DRollQ,New_DYawQ,New_DPitchQ,New_DRollQ,'
                            '_CYawQ,_CPitchQ,_CRollQ,New_CYawQ,New_CPitchQ,New_CRollQ,'
                            '_BYawQ,_BPitchQ,_BRollQ,New_BYawQ,New_BPitchQ,New_BRollQ,'
                            '_AYawQ,_APitchQ,_ARollQ,New_AYawQ,New_APitchQ,New_ARollQ,'
                            '_GYawQ,_GPitchQ,_GRollQ,New_GYawQ,New_GPitchQ,New_GRollQ,'
                            '_NYawQ,_NPitchQ,_NRollQ,New_NYawQ,New_NPitchQ,New_NRollQ,'
                            '_FYawQ,_FPitchQ,_FRollQ,New_FYawQ,New_FPitchQ,New_FRollQ,\n')
                        for device in device_list:
                            prevyaw[device] = 0.0
                            nyaw[device] = 0
                            prevroll[device] = 0.0
                            nroll[device] = 0
                            prevpitch[device] = 0.0
                            npitch[device] = 0

                            d[device] = []
                            data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
                            prevdata[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
                        csvreader = csv.reader(fileold)
                        header = next(csvreader)
                        print(header) #+26
                        rows = []
                        rowcount = 0
                        for row in csvreader:
                            rows.append(row)
                            # print(row[19])
                            towrite = row[19] + ',' + str(int(row[19]) * 100) + ','
                            # print(towrite)
                            # print(header[19])
                            number = 0
                            # print(header[24+1*26:47+1*26])
                            for sensor in device_list:
                                d[sensor] = row[24 + number * 26:47 + number * 26]
                                towrite = towrite + str(d[sensor][calcYaw]) + ',' + str(d[sensor][calcPitch]) + ',' + str(d[sensor][calcRoll]) + ','
                                prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
                                prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
                                # prevpitch[sensor], d[sensor][calcPitch], npitch[sensor] = utils.correctPitch(prevpitch[sensor], d[sensor][calcPitch], npitch[sensor])
                                towrite = towrite + str(d[sensor][calcYaw]) + ',' + str(d[sensor][calcPitch]) + ',' + str(d[sensor][calcRoll]) + ','
                                number += 1
                            filenew.write(towrite + '\n')
                            rowcount += 1
                            print(rowcount)

                    dest_path = utils.add_gait_cycle(os.path.join(dest_dir, folder, newgaitcycle), os.path.join(dest_dir, folder, newfile), "", 1)

