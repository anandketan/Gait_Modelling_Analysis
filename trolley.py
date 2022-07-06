# for no camera
# preetham string

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
right_shoulder, rsport = 'A', 5555
back, backport = 'D', 8888

right_thigh, rtport = 'F', 9000

# writes = 0
# writeCounter = 0
# writeRate = 0

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
UDP_IP = "192.168.1.104"
UDP_PORT = 8500
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pose_detect = ""
step = 0
reach = 0
forward = 0
side = 0

joint_device = {'button': button, 'right_shoulder': right_shoulder, 'back': back, 'right_thigh': right_thigh}

device_list = [button, right_shoulder, back, right_thigh]
port_list = [buttonport, rsport, backport, rtport]

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

sockets = {'button': socks[button], 'right_shoulder': socks[right_shoulder], 'back': socks[back], 'right_thigh': socks[right_thigh]}

init = time.time()
lastthighroll = -90
lastgravYhand = -10
state = "stop"
placeState = "place"
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
        if sensor not in [button]:
            prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw],
                                                                                 nyaw[sensor])
            prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor],
                                                                                     d[sensor][calcRoll], nroll[sensor])

    pose_detect = "pick|right|gravY={}|yaw={}".format(float(d[right_shoulder][gravaccy]), (float(d[right_shoulder][calcYaw]) - float(d[back][calcYaw])))
    # print("last = {}; current = {}".format(lastthighroll, float(d[right_thigh][calcRoll])))
    if lastthighroll >= -135 > float(d[right_thigh][calcRoll]):
        state = 'forward'
    elif lastthighroll < -135 <= float(d[right_thigh][calcRoll]):
        state = 'stop'
    # sockUDP.sendto(state.encode(), (UDP_IP, UDP_PORT))
    lastthighroll = float(d[right_thigh][calcRoll])


    if lastgravYhand > -8 >= float(d[right_shoulder][gravaccy]):
        # print("Place")
        placeState = 'place'
        # sockUDP.sendto("place".encode(), (UDP_IP, UDP_PORT))
    elif lastgravYhand <= -8 < float(d[right_shoulder][gravaccy]):
        placeState = 'no place'
        # print("Sending pick")
        # sockUDP.sendto(pose_detect.encode(), (UDP_IP, UDP_PORT))


    lastgravYhand = float(d[right_shoulder][gravaccy])

    finalstring = placeState + '|' + state + '|' + pose_detect
    print(finalstring)
    sockUDP.sendto(finalstring.encode(), (UDP_IP, UDP_PORT))
