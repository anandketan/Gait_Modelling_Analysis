import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import math
import datetime
from datetime import datetime
import os
import keyboard
# import pressure_sensor_gait_cycle as gait
import utils_sensor_data as utils


def listenfordata(sensor, location):
    try:
        data[sensor] = sockets[location].recv(1024).decode("utf-8")
        prevdata[sensor] = data[sensor]
        flags[sensor] = 1
        if count[sensor] == 0:
            initialtime[sensor] = time.time()
            if sensor != button:
                sendinitialtime[sensor] = int(str(data[sensor]).split(',')[timer])
        count[sensor] += 1
        if time.time() - initialtime[sensor] > 1:
            rate[sensor] = count[sensor] / (time.time() - initialtime[sensor])
            if sensor != button:
                sendrate[sensor] = 1000 * count[sensor] / (int(str(data[sensor]).split(',')[timer]) - sendinitialtime[sensor])
            count[sensor] = 0
    except socket.error:
        data[sensor] = prevdata[sensor]
        flags[sensor] = 0

    d[sensor] = str(data[sensor]).split(',')
    d_raw[sensor] = d[sensor]


def listenconcise(sensor, location):
    try:
        data[sensor] = sockets[location].recv(1024).decode("utf-8")
        prevdata[sensor] = data[sensor]
    except socket.error:
        data[sensor] = prevdata[sensor]
    d[sensor] = str(data[sensor]).split(',')
    d_raw[sensor] = d[sensor]

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

#  display_values => number of values to display at once on the plot
display_values = 500
x = np.linspace(0, display_values, display_values)

y_keys = ['Roll', 'Roll_corrected', 'Pitch', 'Yaw', 'Yaw_corrected',
          'Roll-ref', 'Roll_corrected-ref', 'Pitch-ref', 'Yaw-ref', 'Yaw_corrected-ref',
          'Acc_grav_X', 'Acc_grav_Y', 'Acc_grav_Z', 'sample_limit']

y = {xx: [np.zeros(display_values)] for xx in y_keys}

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-360, 360])
# line1, = ax.plot(x, y['Roll'], label='Roll-raw')
line1, = ax.plot(x, y['Roll_corrected'][0], label='Roll-corrected')
line2, = ax.plot(x, y['Pitch'][0], label='Pitch-raw')
# line3, = ax.plot(x, y['Yaw'][0], label='Yaw-raw')
line3, = ax.plot(x, y['Yaw_corrected'][0], label='Yaw-corrected')
# line1, = ax.plot(x, y['Acc_grav_X'][0], label='Acc_due_to_grav-X')
# line2, = ax.plot(x, y['Acc_grav_Y'][0], label='Acc_due_to_grav-Y')
# line3, = ax.plot(x, y['Acc_grav_Z'][0], label='Acc_due_to_grav-Z')
line4, = ax.plot(x, y['sample_limit'][0], label='button')

ax.legend()

#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases

r = 50
k = 0
counter = 0
looprate = 0

button, buttonport = 'E', 9999
right_shoulder, rsport = 'A', 5555
back, backport = 'D', 8888

name = "Zero_Reference"
joint = "Shoulder"
trial = input("Trial number?\n")
file_name_all = '{}_{}_referenceData_{}_{}_{}_{}.csv'.format(name,
                                                             trial,
                                                             datetime.now().date(),
                                                             datetime.now().time().hour,
                                                             datetime.now().time().minute,
                                                             datetime.now().time().second)
file_name_csv = 'angles_{}_{}.csv'.format(name, trial)
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir,
                        'Reference_data',
                        '{}'.format(joint),
                        '{}'.format(datetime.now().date()))
try:
    os.makedirs(dest_dir)
except OSError:
    pass  # already exists
path_csv = os.path.join(dest_dir, file_name_csv)

writeCounter = 0
writeRate = 0
writes = 0

joint_device = {'button': button, 'right_shoulder': right_shoulder, 'back': back}

device_list = [button, right_shoulder, back]
port_list = [buttonport, rsport, backport]

prevdata = {}
data = {}
d = {}
d_raw = {}

prevyaw = {}
nyaw = {}
prevroll = {}
nroll = {}
prevacc = {}
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
    prevacc[device] = 0.0
    npitch[device] = 0

    d[device] = []
    d_raw[device] = []
    if device != button:
        data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        prevdata[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
    else:
        data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        prevdata[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(3)]
for port, sock in zip(port_list, sock_list):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    sock.setblocking(0)

socks = {}
for device, sock in zip(device_list, sock_list):
    socks[device] = sock

sockets = {'button': socks[button], 'right_shoulder': socks[right_shoulder], 'back': socks[back]}

with open(path_csv, 'w') as file1:
    file1.write('Roll,Roll_corrected,Pitch,Yaw,Yaw_corrected,Roll-ref,Roll_corrected-ref,Pitch-ref,Yaw-ref,Yaw_corrected-ref,Acc_grav_X,Acc_grav_Y,Acc_grav_Z,sample_limit\n')
    init = time.time()
    while not keyboard.is_pressed("q"):
        if counter == 0:
            cur_time = time.time()
        counter += 1
        if time.time() - cur_time > 1:
            looprate = counter / (time.time() - cur_time)
            counter = 0

        for sensor, location in zip(device_list, sockets):
            listenfordata(sensor, location)

        for sensor in device_list:
            if sensor not in [button]:
                prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
                prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])

        y['Roll'][0] = np.roll(y['Roll'][0], -1)
        y['Roll'][0][-1] = float(d_raw[right_shoulder][calcRoll])  # Raw Roll

        y['Roll_corrected'][0] = np.roll(y['Roll_corrected'][0], -1)
        y['Roll_corrected'][0][-1] = d[right_shoulder][calcRoll]  # Corrected Roll

        y['Pitch'][0] = np.roll(y['Pitch'][0], -1)
        y['Pitch'][0][-1] = float(d[right_shoulder][calcPitch])  # Raw Pitch

        y['Yaw'][0] = np.roll(y['Yaw'][0], -1)
        y['Yaw'][0][-1] = float(d_raw[right_shoulder][calcYaw])  # Raw Yaw

        y['Yaw_corrected'][0] = np.roll(y['Yaw_corrected'][0], -1)
        y['Yaw_corrected'][0][-1] = d[right_shoulder][calcYaw]  # Corrected Yaw

        y['Roll-ref'][0] = np.roll(y['Roll-ref'][0], -1)
        y['Roll-ref'][0][-1] = float(d_raw[right_shoulder][calcRoll]) - float(d_raw[back][calcRoll])  # Raw Roll

        y['Roll_corrected-ref'][0] = np.roll(y['Roll_corrected-ref'][0], -1)
        y['Roll_corrected-ref'][0][-1] = d[right_shoulder][calcRoll] - float(d[back][calcRoll])  # Corrected Roll

        y['Pitch-ref'][0] = np.roll(y['Pitch-ref'][0], -1)
        y['Pitch-ref'][0][-1] = float(d[right_shoulder][calcPitch]) - float(d[back][calcPitch])  # Raw Pitch

        y['Yaw-ref'][0] = np.roll(y['Yaw-ref'][0], -1)
        y['Yaw-ref'][0][-1] = float(d_raw[right_shoulder][calcYaw]) - float(d_raw[back][calcYaw])  # Raw Yaw

        y['Yaw_corrected-ref'][0] = np.roll(y['Yaw_corrected-ref'][0], -1)
        y['Yaw_corrected-ref'][0][-1] = d[right_shoulder][calcYaw] - float(d[back][calcYaw])  # Corrected Yaw

        y['Acc_grav_X'][0] = np.roll(y['Acc_grav_X'][0], -1)
        y['Acc_grav_X'][0][-1] = d[right_shoulder][gravaccx]

        y['Acc_grav_Y'][0] = np.roll(y['Acc_grav_Y'][0], -1)
        y['Acc_grav_Y'][0][-1] = d[right_shoulder][gravaccy]

        y['Acc_grav_Z'][0] = np.roll(y['Acc_grav_Z'][0], -1)
        y['Acc_grav_Z'][0][-1] = d[right_shoulder][gravaccz]

        y['sample_limit'][0] = np.roll(y['sample_limit'][0], -1)
        y['sample_limit'][0][-1] = int(d[button][hs]) * 100  # button * 100

        if flags[right_shoulder]:
            writes += 1
            if writeCounter == 0:
                write_cur_time = time.time()
            writeCounter += 1
            if time.time() - write_cur_time > 1:
                writeRate = writeCounter / (time.time() - write_cur_time)
                writeCounter = 0
            timeWrite = time.time() - init

            file1.write(str(y['Roll'][0][-1]) + ',' + str(y['Roll_corrected'][0][-1]) + ',' +
                        str(y['Pitch'][0][-1]) + ',' +
                        str(y['Yaw'][0][-1]) + ',' + str(y['Yaw_corrected'][0][-1]) + ',' +
                        str(y['Roll-ref'][0][-1]) + ',' + str(y['Roll_corrected-ref'][0][-1]) + ',' +
                        str(y['Pitch-ref'][0][-1]) + ',' +
                        str(y['Yaw-ref'][0][-1]) + ',' + str(y['Yaw_corrected-ref'][0][-1]) + ',' +
                        str(y['Acc_grav_X'][0][-1]) + ',' + str(y['Acc_grav_Y'][0][-1]) + ',' + str(y['Acc_grav_Z'][0][-1]) + ',' +
                        str(y['sample_limit'][0][-1]) + '\n')

        k = k + 1
        if k == r:
            # line1.set_ydata(y['Roll'])
            line1.set_ydata(y['Roll_corrected'])
            line2.set_ydata(y['Pitch'])
            # line3.set_ydata(y['Yaw'])
            line3.set_ydata(y['Yaw_corrected'])
            # line1.set_ydata(y['Acc_grav_X'])
            # line2.set_ydata(y['Acc_grav_Y'])
            # line3.set_ydata(y['Acc_grav_Z'])
            line4.set_ydata(y['sample_limit'])
            fig.canvas.draw()
            fig.canvas.flush_events()
            k = 0
