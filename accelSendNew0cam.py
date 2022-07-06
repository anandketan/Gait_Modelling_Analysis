# Game input(copy from laptop)

import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import math
import os
import datetime
from datetime import datetime
import pyrealsense2 as rs
import cv2

import keyboard
import utils_sensor_data as utils


def listenfordata(sensor, location):
    try:
        data[sensor] = sockets[location].recv(1024).decode("utf-8")
        prevdata[sensor] = data[sensor]
        flags[sensor] = 1
        if count[sensor] == 0:
            initialtime[sensor] = time.time()
            if sensor != 'E':
                sendinitialtime[sensor] = int(str(data[sensor]).split(',')[timer])
        count[sensor] += 1
        if time.time() - initialtime[sensor] > 1:
            rate[sensor] = count[sensor] / (time.time() - initialtime[sensor])
            if sensor != 'E':
                sendrate[sensor] = 1000 * count[sensor] / (int(str(data[sensor]).split(',')[timer]) - sendinitialtime[sensor])
            count[sensor] = 0
    except socket.error:
        data[sensor] = prevdata[sensor]
        flags[sensor] = 0

    d[sensor] = str(data[sensor]).split(',')


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

counter = 0
k = 0
looprate = 0

writes = 0
writeCounter = 0
writeRate = 0

name = 'Test'
trial = input("Trial number?\n")
file_name_all = '{}_{}_allGameSensorData_{}_{}_{}_{}.csv'.format(name, trial, datetime.now().date(),
                                                                 datetime.now().time().hour,
                                                                 datetime.now().time().minute,
                                                                 datetime.now().time().second)
file_name_pose = 'diff_pitch_{}_{}.csv'.format(name, trial)
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}'.format(datetime.now().date()), '{}_{}'.format(name, trial))
try:
    os.makedirs(dest_dir)
except OSError:
    pass  # already exists
path_game = os.path.join(dest_dir, file_name_all)
path_pose = os.path.join(dest_dir, file_name_pose)

# UDP_IP = "192.168.100.1"
UDP_IP = "127.0.0.1"
UDP_PORT = 5065
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pose_detect = ""
step = 0
reach = 0
forward = 0
side = 0

device_list = ['B', 'C', 'F', 'D', 'H']
port_list = [6666, 7777, 9000, 8888, 8000]

prevdata = {}
data = {}
d = {}

prevyaw = {}
nyaw = {}
prevroll = {}
nroll = {}
prevpitch = {}
npitch = {}

flags = {}
count = {}
initialtime = {}
rate = {}
sendrate = {}
sendinitialtime = {}

for device in device_list:
    flags[device] = 0
    count[device] = 0
    initialtime[device] = 0.0
    rate[device] = 0.0
    sendrate[device] = 0.0
    sendinitialtime[device] = 0.0

    prevyaw[device] = 0.0
    nyaw[device] = 0
    prevroll[device] = 0.0
    nroll[device] = 0
    prevpitch[device] = 0.0
    npitch[device] = 0

    d[device] = []
    data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
    prevdata[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(5)]
for port, sock in zip(port_list, sock_list):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    sock.setblocking(0)

socks = {}
for device, sock in zip(device_list, sock_list):
    socks[device] = sock

sockets = {'right_bicep': socks['B'], 'right_thigh': socks['C'], 'right_shank': socks['F'], 'back': socks['D'],
           'right_forearm': socks['H']}

with open(os.path.join(dest_dir, 'device_list.txt'), 'w') as f:
    f.write(str(device_list) + '\n')
    f.write(str(port_list) + '\n')
    f.write(str(sockets) + '\n')

with open(path_pose, 'w') as file1, open(path_game, 'w') as file2:
    file1.write('count,'
                'RAUGravAccX,RAUGravAccY,RAUGravAccZ,RALGravAccX,RALGravAccY,RALGravAccZ,'
                'RA_diff_roll,RA_diff_pitch,RA_diff_yaw,Reach,'
                'RLUGravAccX,RLUGravAccY,RLUGravAccZ,RLLGravAccX,RLLGravAccY,RLLGravAccZ,'
                'RL_diff_roll,RL_diff_pitch,RL_diff_yaw,Step,'
                'BackGravAccX,BackGravAccY,BackGravAccZ,Back_roll,Back_pitch,Back_yaw,Forward,Sway'
                '\n')
    file2.write('count,'
                'FlagD,AccX_D,AccY_D,AccZ_D,GyroX_D,GyroY_D,GyroZ_D,_DQ1,_DQ2,_DQ3,_DQ4,_DYawQ,_DPitchQ,_DRollQ,_DYaw,_DPitch,_DRoll,_Dcount,_Dtime,_DHS,_DDist,_DgravaccX,_DgravaccY,_DgravaccZ,_DSendRate,_DRecvRate,'
                'FlagC,AccX_C,AccY_C,AccZ_C,GyroX_C,GyroY_C,GyroZ_C,_CQ1,_CQ2,_CQ3,_CQ4,_CYawQ,_CPitchQ,_CRollQ,_CYaw,_CPitch,_CRoll,_Ccount,_Ctime,_CHS,_CDist,_CgravaccX,_CgravaccY,_CgravaccZ,_CSendRate,_CRecvRate,'
                'FlagB,AccX_B,AccY_B,AccZ_B,GyroX_B,GyroY_B,GyroZ_B,_BQ1,_BQ2,_BQ3,_BQ4,_BYawQ,_BPitchQ,_BRollQ,_BYaw,_BPitch,_BRoll,_Bcount,_Btime,_BHS,_BDist,_BgravaccX,_BgravaccY,_BgravaccZ,_BSendRate,_BRecvRate,'
                'FlagG,AccX_G,AccY_G,AccZ_G,GyroX_G,GyroY_G,GyroZ_G,_GQ1,_GQ2,_GQ3,_GQ4,_GYawQ,_GPitchQ,_GRollQ,_GYaw,_GPitch,_GRoll,_Gcount,_Gtime,_GHS,_GDist,_GgravaccX,_GgravaccY,_GgravaccZ,_GSendRate,_GRecvRate,'
                'FlagN,AccX_N,AccY_N,AccZ_N,GyroX_N,GyroY_N,GyroZ_N,_NQ1,_NQ2,_NQ3,_NQ4,_NYawQ,_NPitchQ,_NRollQ,_NYaw,_NPitch,_NRoll,_Ncount,_Ntime,_NHS,_NDist,_NgravaccX,_NgravaccY,_NgravaccZ,_NSendRate,_NRecvRate,'
                'writeRate,rate,time' + '\n')
    init = time.time()
    while not keyboard.is_pressed("q"):  # time.time() - init <=10
        if counter == 0:
            cur_time = time.time()
        counter += 1
        if time.time() - cur_time > 1:
            looprate = counter / (time.time() - cur_time)
            counter = 0

        # print("Loop", looprate)

        for sensor, location in zip(device_list, sockets):
            listenfordata(sensor, location)

        for sensor in device_list:
            prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
            prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
            prevpitch[sensor], d[sensor][calcPitch], npitch[sensor] = utils.correctPitch(prevpitch[sensor], d[sensor][calcPitch], npitch[sensor])

        pose_detect = str(d['D'][gravaccx]) + "," + str(d['D'][gravaccy]) + "," + str(d['D'][gravaccz]) + "," + \
                      str(d['B'][gravaccx]) + "," + str(d['B'][gravaccy]) + "," + str(d['B'][gravaccz]) + "," + \
                      str(d['H'][gravaccx]) + "," + str(d['H'][gravaccy]) + "," + str(d['H'][gravaccz]) + "," + \
                      str(d['C'][gravaccx]) + "," + str(d['C'][gravaccy]) + "," + str(d['C'][gravaccz]) + "," + \
                      str(d['F'][gravaccx]) + "," + str(d['F'][gravaccy]) + "," + str(d['F'][gravaccz])

        sockUDP.sendto(pose_detect.encode(), (UDP_IP, UDP_PORT))
        print(pose_detect)

        raRoll = d['B'][calcRoll] - d['H'][calcRoll]
        raYaw = d['B'][calcYaw] - d['H'][calcYaw]
        raPitch = d['B'][calcPitch] - d['H'][calcPitch]
        rlRoll = d['C'][calcRoll] - d['F'][calcRoll]
        rlYaw = d['C'][calcYaw] - d['F'][calcYaw]
        rlPitch = d['C'][calcPitch] - d['F'][calcPitch]

        if float(d['B'][gravaccx]) > 2.5 and float(d['H'][gravaccx]) > 2.5 and float(d['B'][gravaccy]) < 0:
            reach = 1
        else:
            reach = 0

        if ((float(d['C'][gravaccz]) < 0 and float(d['F'][gravaccz]) < 0) or float(d['C'][gravaccz]) < -2 or float(
                d['F'][gravaccz]) < -2) and (float(d['C'][gravaccy]) > -2.5 and float(d['C'][gravaccy]) < 2.5) and (
                float(d['F'][gravaccy]) > -2.5 and float(d['F'][gravaccy]) < 2.5) and float(
                d['C'][gravaccx]) < 0 and float(d['C'][gravaccx]) < 0:
            step = 1
            # print("Step")
        else:
            step = 0
            # print("No Step")

        if flags['F'] or flags['C'] or flags['B'] or flags['D'] or flags['H']:
            writes += 1
            if writeCounter == 0:
                write_cur_time = time.time()
            writeCounter += 1
            if time.time() - write_cur_time > 1:
                writeRate = writeCounter / (time.time() - write_cur_time)
                writeCounter = 0
            # print("write", writeRate)
            timeWrite = time.time() - init

            file2.write(str(writes) + ',' +
                        str(flags['B']) + ',' + str(data['B']) + ',' + str(sendrate['B']) + ',' + str(rate['B']) + ',' +
                        str(flags['C']) + ',' + str(data['C']) + ',' + str(sendrate['C']) + ',' + str(rate['C']) + ',' +
                        str(flags['F']) + ',' + str(data['F']) + ',' + str(sendrate['F']) + ',' + str(rate['F']) + ',' +
                        str(flags['D']) + ',' + str(data['D']) + ',' + str(sendrate['D']) + ',' + str(rate['D']) + ',' +
                        str(flags['H']) + ',' + str(data['H']) + ',' + str(sendrate['H']) + ',' + str(rate['H']) + ',' +
                        str(writeRate) + ',' + str(looprate) + ',' + str(timeWrite) + '\n')

            file1.write(str(writes) + ',' +
                        str(d['F'][gravaccx]) + ',' + str(d['F'][gravaccy]) + ',' + str(d['F'][gravaccz]) + ',' +
                        str(d['H'][gravaccx]) + ',' + str(d['H'][gravaccy]) + ',' + str(d['H'][gravaccz]) + ',' +
                        str(raRoll) + ',' + str(raPitch) + ',' + str(raYaw) + ',' + str(reach) + ',' +
                        str(d['C'][gravaccx]) + ',' + str(d['C'][gravaccy]) + ',' + str(d['C'][gravaccz]) + ',' +
                        str(d['F'][gravaccx]) + ',' + str(d['F'][gravaccy]) + ',' + str(d['F'][gravaccz]) + ',' +
                        str(rlRoll) + ',' + str(rlPitch) + ',' + str(rlYaw) + ',' + str(step) + ',' +
                        str(d['D'][gravaccx]) + ',' + str(d['D'][gravaccy]) + ',' + str(d['D'][gravaccz]) + ',' +
                        str(d['D'][calcRoll]) + ',' + str(d['D'][calcPitch]) + ',' + str(d['D'][calcYaw]) + ',' +
                        str(forward) + ',' + str(side) + ',' + '\n')
