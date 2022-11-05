# correction for yaw/picth/roll after collection from raw data of game

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

device_list = ['B', 'C', 'F', 'D', 'H']

prevdata = {}
data = {}
d = {}
prevyaw = {}
nyaw = {}
prevroll = {}
nroll = {}
prevpitch = {}
npitch = {}



i = 0
date = ['2022-03-29', '2022-03-30', '2022-03-31']
for day in date:
    dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}'.format(day))
    for folder in os.listdir(dest_dir):
        if '.csv' not in folder and '.png' not in folder:
        # try:
            os.listdir(os.path.join(dest_dir, folder))
            i += 1
            for file in os.listdir(os.path.join(dest_dir, folder)):
                if 'allGameSensorData' in file:
                    print(i, file)
                    newfile = file.split('_')[0] + file.split('_')[1] + 'corrected.csv'
                    with open(os.path.join(dest_dir, folder, newfile), 'w') as filenew, open(os.path.join(dest_dir, folder, file), 'r') as fileold:
                        filenew.write('_DYawQ,_DPitchQ,_DRollQ,New_DYawQ,New_DPitchQ,New_DRollQ,'
                                      '_CYawQ,_CPitchQ,_CRollQ,New_CYawQ,New_CPitchQ,New_CRollQ,'
                                      '_BYawQ,_BPitchQ,_BRollQ,New_BYawQ,New_BPitchQ,New_BRollQ,'
                                      '_GYawQ,_GPitchQ,_GRollQ,New_GYawQ,New_GPitchQ,New_GRollQ,'
                                      '_NYawQ,_NPitchQ,_NRollQ,New_NYawQ,New_NPitchQ,New_NRollQ,\n')
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
                        for row in csvreader:
                            rows.append(row)
                            towrite = ''
                            number = 0
                            # print(header[2+0*26:25+0*26])
                            for sensor in device_list:
                                d[sensor] = row[2 + number * 26:25 + number * 26]
                                towrite = towrite + str(d[sensor][calcYaw]) + ',' + str(d[sensor][calcPitch]) + ',' + str(d[sensor][calcRoll]) + ','
                                prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
                                prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
                                prevpitch[sensor], d[sensor][calcPitch], npitch[sensor] = utils.correctPitch(prevpitch[sensor], d[sensor][calcPitch], npitch[sensor])
                                towrite = towrite + str(d[sensor][calcYaw]) + ',' + str(d[sensor][calcPitch]) + ',' + str(d[sensor][calcRoll]) + ','
                                number += 1
                            filenew.write(towrite + '\n')

        # except:
        #     pass
