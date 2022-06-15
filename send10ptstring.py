# for no camera

import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import math
import os
import datetime
from datetime import datetime
# import pyrealsense2 as rs
# import cv2

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
packetCount = 16
timer = 17
hs = 18
dist = 19
gravaccx = 20
gravaccy = 21
gravaccz = 22

counter = 0
k = 0
looprate = 0

noOfSensors = 4

button, buttonport = 'E', 9999
right_shoulder, rsport = 'H', 8000
back, backport = 'D', 8888

# name = 'test'
# trial = input("Trial number?\n")
# file_name_all = '{}_{}_allGameSensorData_{}_{}_{}_{}.csv'.format(name, trial, datetime.now().date(),
#                                                                  datetime.now().time().hour,
#                                                                  datetime.now().time().minute,
#                                                                  datetime.now().time().second)
# script_dir = os.path.dirname(os.path.abspath(__file__))
# dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}'.format(datetime.now().date()), '{}_{}'.format(name, trial))
# try:
#     os.makedirs(dest_dir)
# except OSError:
#     pass  # already exists
# path_game = os.path.join(dest_dir, file_name_all)

# UDP_IP = "192.168.100.1"
UDP_IP = "192.168.1.101"
UDP_PORT = 8500
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pose_detect = ""
step = 0
reach = 0
forward = 0
side = 0

joint_device = {'button': button, 'right_shoulder': right_shoulder, 'back': back}

device_list = [button, right_shoulder, back]
port_list = [buttonport, rsport, backport]

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

sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(noOfSensors)]
for port, sock in zip(port_list, sock_list):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    sock.setblocking(0)

socks = {}
for device, sock in zip(device_list, sock_list):
    socks[device] = sock

sockets = {'button': socks[button], 'right_shoulder': socks[right_shoulder], 'back': socks[back]}

# with open(path_game, 'w') as file2:
#     file2.write('count,'
#                 '_NYawQ,_NPitchQ,_NRollQ,'
#                 'writeRate,rate,time' + '\n')
init = time.time()
samplecount = 0
pose_detect = ""
poses = []
prevHS = 0
while samplecount < 10:  # time.time() - init <=10
    for sensor, location in zip(device_list, sockets):
        listenfordata(sensor, location)

    if prevHS == 0 and int(d[button][hs]) == 1:
        poses.extend([float(d[right_shoulder][gravaccy]), float(d[right_shoulder][calcYaw])])
        samplecount += 1
        print(samplecount)

    prevHS = int(d[button][hs])
print(poses)
# pose_detect = "start right " \
#               "roll={} pitch={} yaw={} roll={} pitch={} yaw={} roll={} pitch={} yaw={} " \
#               "roll={} pitch={} yaw={} roll={} pitch={} yaw={} roll={} pitch={} yaw={} " \
#               "roll={} pitch={} yaw={} roll={} pitch={} yaw={} roll={} pitch={} yaw={} " \
#               "roll={} pitch={} yaw={}".format(poses[0][0], poses[0][1], poses[0][2], poses[1][0], poses[1][1], poses[1][2], poses[2][0], poses[2][1], poses[2][2],
#                                                poses[3][0], poses[3][1], poses[3][2], poses[4][0], poses[4][1], poses[4][2], poses[5][0], poses[5][1], poses[5][2],
#                                                poses[6][0], poses[6][1], poses[6][2], poses[7][0], poses[7][1], poses[7][2], poses[8][0], poses[8][1], poses[8][2],
#                                                poses[9][0], poses[9][1], poses[9][2])

pose_detect = "start|right|" \
              "gravY={}|Yaw={}|gravY={}|Yaw={}|gravY={}|Yaw={}|gravY={}|Yaw={}|gravY={}|Yaw={}|" \
              "gravY={}|Yaw={}|gravY={}|Yaw={}|gravY={}|Yaw={}|gravY={}|Yaw={}|gravY={}|Yaw={}".format(poses[0], poses[1],
                                                                                                       poses[2], poses[3],
                                                                                                       poses[4], poses[5],
                                                                                                       poses[6], poses[7],
                                                                                                       poses[8], poses[9],
                                                                                                       poses[10],
                                                                                                       poses[11],
                                                                                                       poses[12],
                                                                                                       poses[13],
                                                                                                       poses[14],
                                                                                                       poses[15],
                                                                                                       poses[16],
                                                                                                       poses[17],
                                                                                                       poses[18],
                                                                                                       poses[19]
                                                                                                       )

# print(poses)
print(pose_detect)
for i in range(10):
    sockUDP.sendto(pose_detect.encode(), (UDP_IP, UDP_PORT))
