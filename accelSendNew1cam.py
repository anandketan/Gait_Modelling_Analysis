# for 1 camera

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
count = 16
timer = 17
hs = 18
dist = 19
gravaccx = 20
gravaccy = 21
gravaccz = 22

counter = 0
k = 0
looprate = 0

i = 0
countFrames = 0
rateFrames = 0
initialtimeFrames = 0
frameTime = 0
flagFrames = 0
framepath = ''

writes = 0
writeCounter = 0
writeRate = 0

try:
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
    profile = pipeline.start(config)
    print("Camera ready!!!!!!!!!!!!!!!!!!!!!!!!!")
except:
    print("Camera input not received, connect to other USB port or continue without camera")

name = 'TestFrames'
trial = input("Trial number?\n")
file_name_all = '{}_{}_allGameSensorData_{}_{}_{}_{}.csv'.format(name, trial, datetime.now().date(),
                                                                 datetime.now().time().hour,
                                                                 datetime.now().time().minute,
                                                                 datetime.now().time().second)
file_name_pose = 'diff_pitch_{}_{}.csv'.format(name, trial)
file_name_frames = 'Frames.csv'
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}'.format(datetime.now().date()), '{}_{}'.format(name, trial))
try:
    os.makedirs(dest_dir)
except OSError:
    pass  # already exists
path_game = os.path.join(dest_dir, file_name_all)
path_pose = os.path.join(dest_dir, file_name_pose)
path_frames = os.path.join(dest_dir, file_name_frames)

# UDP_IP = "192.168.100.1"
UDP_IP = "127.0.0.1"
UDP_PORT = 5065
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pose_detect = ""
step = 0
reach = 0
forward = 0
side = 0

device_list = ['D', 'C', 'B', 'G', 'N']
port_list = [8888, 7777, 6666, 4444, 3333]

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

sockets = {'right_bicep': socks['D'], 'right_thigh': socks['C'], 'right_shank': socks['B'], 'back': socks['G'],
           'right_forearm': socks['N']}

with open(path_pose, 'w') as file1, open(path_game, 'w') as file2, open(path_frames, 'w') as file3:
    file1.write('count,FrameNo,FramePath,'
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
                'FlagFrame,FrameNo,FrameRate,FramePath,writeRate,rate,time' + '\n')
    file3.write(
        'Frame,TimeStamp,Rate'
        '\n')
    init = time.time()
    while not keyboard.is_pressed("q"):  # time.time() - init <=10
        if counter == 0:
            cur_time = time.time()
        counter += 1
        if time.time() - cur_time > 1:
            looprate = counter / (time.time() - cur_time)
            counter = 0

        # print("Loop", looprate)

        try:
            frames = pipeline.poll_for_frames()
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            i += 1
            flagFrames = 1
            if countFrames == 0:
                initialtimeFrames = time.time()
            countFrames += 1
            if time.time() - initialtimeFrames > 1:
                rateFrames = countFrames / (time.time() - initialtimeFrames)
                countFrames = 0
        except:
            flagFrames = 0

        for sensor, location in zip(device_list, sockets):
            listenfordata(sensor, location)

        for sensor in device_list:
            prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
            prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
            prevpitch[sensor], d[sensor][calcPitch], npitch[sensor] = utils.correctPitch(prevpitch[sensor], d[sensor][calcPitch], npitch[sensor])

        pose_detect = str(d['G'][gravaccx]) + "," + str(d['G'][gravaccy]) + "," + str(d['G'][gravaccz]) + "," + \
                      str(d['D'][gravaccx]) + "," + str(d['D'][gravaccy]) + "," + str(d['D'][gravaccz]) + "," + \
                      str(d['N'][gravaccx]) + "," + str(d['N'][gravaccy]) + "," + str(d['N'][gravaccz]) + "," + \
                      str(d['C'][gravaccx]) + "," + str(d['C'][gravaccy]) + "," + str(d['C'][gravaccz]) + "," + \
                      str(d['B'][gravaccx]) + "," + str(d['B'][gravaccy]) + "," + str(d['B'][gravaccz])

        sockUDP.sendto(pose_detect.encode(), (UDP_IP, UDP_PORT))
        print(pose_detect)

        raRoll = d['D'][calcRoll] - d['N'][calcRoll]
        raYaw = d['D'][calcYaw] - d['N'][calcYaw]
        raPitch = d['D'][calcPitch] - d['N'][calcPitch]
        rlRoll = d['C'][calcRoll] - d['B'][calcRoll]
        rlYaw = d['C'][calcYaw] - d['B'][calcYaw]
        rlPitch = d['C'][calcPitch] - d['B'][calcPitch]

        if float(d['D'][gravaccx]) > 2.5 and float(d['N'][gravaccx]) > 2.5 and float(d['D'][gravaccy]) < 0:
            reach = 1
        else:
            reach = 0

        if ((float(d['C'][gravaccz]) < 0 and float(d['B'][gravaccz]) < 0) or float(d['C'][gravaccz]) < -2 or float(
                d['B'][gravaccz]) < -2) and (float(d['C'][gravaccy]) > -2.5 and float(d['C'][gravaccy]) < 2.5) and (
                float(d['B'][gravaccy]) > -2.5 and float(d['B'][gravaccy]) < 2.5) and float(
                d['C'][gravaccx]) < 0 and float(d['C'][gravaccx]) < 0:
            step = 1
            # print("Step")
        else:
            step = 0
            # print("No Step")

        if flags['B'] or flags['C'] or flags['D'] or flags['G'] or flags['N'] or flagFrames:
            writes += 1
            if writeCounter == 0:
                write_cur_time = time.time()
            writeCounter += 1
            if time.time() - write_cur_time > 1:
                writeRate = writeCounter / (time.time() - write_cur_time)
                writeCounter = 0
            # print("write", writeRate)
            timeWrite = time.time() - init
            if flagFrames:
                cv2.putText(color_image, "{}".format(timeWrite), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                            cv2.LINE_AA)
                cv2.putText(color_image, "{}".format(i), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                            cv2.LINE_AA)
                framepath = f'{dest_dir}/Frame_{i}_' + str(timeWrite) + '.jpg'
                cv2.imwrite(framepath, color_image)
                # cv2.imshow('BGR feed', color_image)
                # key = cv2.waitKey(1)
                file3.write(str(i) + ',' + str(timeWrite) + ',' + str(rateFrames) + '\n')
                # print(rateFrames)
            file2.write(str(writes) + ',' +
                        str(flags['D']) + ',' + str(data['D']) + ',' + str(sendrate['D']) + ',' + str(rate['D']) + ',' +
                        str(flags['C']) + ',' + str(data['C']) + ',' + str(sendrate['C']) + ',' + str(rate['C']) + ',' +
                        str(flags['B']) + ',' + str(data['B']) + ',' + str(sendrate['B']) + ',' + str(rate['B']) + ',' +
                        str(flags['G']) + ',' + str(data['G']) + ',' + str(sendrate['G']) + ',' + str(rate['G']) + ',' +
                        str(flags['N']) + ',' + str(data['N']) + ',' + str(sendrate['N']) + ',' + str(rate['N']) + ',' +
                        str(flagFrames) + ',' + str(i) + ',' + str(rateFrames) + ',' +
                        str('=HYPERLINK(\"{}\")'.format(framepath)) + ',' + str(writeRate) + ',' + str(looprate) + ',' +
                        str(timeWrite) + '\n')
            
            file1.write(str(writes) + ',' + str(i) + ',' + str('=HYPERLINK(\"{}\")'.format(framepath)) + ',' +
                        str(d['B'][gravaccx]) + ',' + str(d['B'][gravaccy]) + ',' + str(d['B'][gravaccz]) + ',' + 
                        str(d['N'][gravaccx]) + ',' + str(d['N'][gravaccy]) + ',' + str(d['N'][gravaccz]) + ',' +
                        str(raRoll) + ',' + str(raPitch) + ',' + str(raYaw) + ',' + str(reach) + ',' +
                        str(d['C'][gravaccx]) + ',' + str(d['C'][gravaccy]) + ',' + str(d['C'][gravaccz]) + ',' +
                        str(d['B'][gravaccx]) + ',' + str(d['B'][gravaccy]) + ',' + str(d['B'][gravaccz]) + ',' +
                        str(rlRoll) + ',' + str(rlPitch) + ',' + str(rlYaw) + ',' + str(step) + ',' +
                        str(d['G'][gravaccx]) + ',' + str(d['G'][gravaccy]) + ',' + str(d['G'][gravaccz]) + ',' +
                        str(d['G'][calcRoll]) + ',' + str(d['G'][calcPitch]) + ',' + str(d['G'][calcYaw]) + ',' +
                        str(forward) + ',' + str(side) + ',' + '\n')
