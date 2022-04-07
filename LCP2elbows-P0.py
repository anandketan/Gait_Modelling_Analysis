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


def listenconcise(sensor, location):
    try:
        data[sensor] = sockets[location].recv(1024).decode("utf-8")
        prevdata[sensor] = data[sensor]
    except socket.error:
        data[sensor] = prevdata[sensor]
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

#  display_values => number of values to display at once on the plot
display_values = 500
x = np.linspace(0, display_values, display_values)

y = [np.zeros(display_values)]*20

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-180, 180])
line1, = ax.plot(x, y[0], 'b-', label='rollrighttricep')
line2, = ax.plot(x, y[1], 'r-', label='rollrightforearm')
line3, = ax.plot(x, y[2], 'y-', label='flexangleRight')
line4, = ax.plot(x, y[3], 'g-', label='rolllefttricep')
line5, = ax.plot(x, y[4], 'm-', label='rollleftforearm')
line6, = ax.plot(x, y[5], 'k-', label='flexangleLeft')
# line7, = ax.plot(x, y[6], 'c-', label='accZ-C')
# line8, = ax.plot(x, y[7], 'tab:pink', label='nB')
line9, = ax.plot(x, y[19], 'tab:gray', label='hs-US')
line10, = ax.plot(x, y[9], 'tab:brown', label='hs')
ax.legend()
#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 50
counter = 0
k = 0
rate = 0

button, buttonport = 'E', 9999
right_tricep, rtport = 'D', 8888
right_forearm, rfport = 'C', 7777
left_tricep, ltport = 'B', 6666
left_forearm, lfport = 'A', 5555

# name = input("Name of patient\n")
# joint = input("Name of joint\n")
name = "Test"
joint = "Elbows"
trial = input("Trial number?\n")
file_name_all = '{}_{}_allSensorData_{}_{}_{}_{}.csv'.format(name, trial, datetime.now().date(), datetime.now().time().hour,
                                               datetime.now().time().minute, datetime.now().time().second)
file_name_diff_pitch = 'diff_pitch_{}_{}.csv'.format(name, trial)
file_name_gait_cycle = '{}_{}_gait_cycle.csv'.format(name, trial)
file_name_gait_cycle_US = '{}_{}_gait_cycle_US.csv'.format(name, trial)
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(datetime.now().date()), '{}_{}_gait_cycle'.format(name, trial))
try:
    os.makedirs(dest_dir)
except OSError:
    pass  # already exists
path_all = os.path.join(dest_dir, file_name_all)
path_diff_pitch = os.path.join(dest_dir, file_name_diff_pitch)
path_gait_cycle = os.path.join(dest_dir, file_name_gait_cycle)
path_gait_cycle_US = os.path.join(dest_dir, file_name_gait_cycle_US)

writeCounter = 0
writeRate = 0
writes = 0

calibcounter = 0
calibAngle = {'rightelbowflex': 0, 'rightelbowvar': 0, 'rightelbowrot': 0, 'leftelbowflex': 0, 'leftelbowvar': 0, 'leftelbowrot': 0}

joint_device = {'button': button, 'right_tricep': right_tricep, 'right_forearm': right_forearm, 
                'left_tricep': left_tricep, 'left_forearm': left_forearm}

device_list = [button, right_tricep, right_forearm, left_tricep, left_forearm]
port_list = [buttonport, rtport, rfport, ltport, lfport]

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
    if device != button:
        data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        prevdata[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
    else:
        data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        prevdata[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(5)]
for port, sock in zip(port_list, sock_list):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    sock.setblocking(0)

socks = {}
for device, sock in zip(device_list, sock_list):
    socks[device] = sock

sockets = {'button': socks[button], 'right_tricep': socks[right_tricep], 'right_forearm': socks[right_forearm],
           'left_tricep': socks[left_tricep], 'left_forearm': socks[left_forearm]}

# joint_device = {x: y for (x, y) in zip(sockets, device_list)}

with open(os.path.join(dest_dir, 'device_list.txt'), 'w') as f:
    f.write(str(device_list) + '\n')
    f.write(str(port_list) + '\n')
    # f.write(str(sockets) + '\n')
    f.write(str(joint_device) + '\n')
    f.write('Storage order: {}{}{}{}{}\n'.format(button, right_tricep, right_forearm, left_tricep, left_forearm))

with open(path_diff_pitch, 'w') as file1, open(path_all, 'w') as file2:
    file1.write('RightRoll1,RightRoll2,Rightflex_angle,'
                'RightPitch1,RightPitch2,Rightvar_angle,'
                'RightYaw1,RightYaw2,Rightrot_angle,'
                'LeftRoll1,LeftRoll2,Leftflex_angle,'
                'LeftPitch1,LeftPitch2,Leftvar_angle,'
                'LeftYaw1,LeftYaw2,Leftrot_angle,hs,hs_US\n')
    file2.write(
        'FlagE,AccX_E,AccY_E,AccZ_E,GyroX_E,GyroY_E,GyroZ_E,_EQ1,_EQ2,_EQ3,_EQ4,_EYawQ,_EPitchQ,_ERollQ,_EYaw,_EPitch,_ERoll,_Ecount,_Etime,_EStep,_EDist,_ESendRate,_ERecvRate,'
        'FlagD,AccX_D,AccY_D,AccZ_D,GyroX_D,GyroY_D,GyroZ_D,_DQ1,_DQ2,_DQ3,_DQ4,_DYawQ,_DPitchQ,_DRollQ,_DYaw,_DPitch,_DRoll,_Dcount,_Dtime,_DHS,_DDist,_DgravaccX,_DgravaccY,_DgravaccZ,_DSendRate,_DRecvRate,'
        'FlagC,AccX_C,AccY_C,AccZ_C,GyroX_C,GyroY_C,GyroZ_C,_CQ1,_CQ2,_CQ3,_CQ4,_CYawQ,_CPitchQ,_CRollQ,_CYaw,_CPitch,_CRoll,_Ccount,_Ctime,_CHS,_CDist,_CgravaccX,_CgravaccY,_CgravaccZ,_CSendRate,_CRecvRate,'
        'FlagB,AccX_B,AccY_B,AccZ_B,GyroX_B,GyroY_B,GyroZ_B,_BQ1,_BQ2,_BQ3,_BQ4,_BYawQ,_BPitchQ,_BRollQ,_BYaw,_BPitch,_BRoll,_Bcount,_Btime,_BHS,_BDist,_BgravaccX,_BgravaccY,_BgravaccZ,_BSendRate,_BRecvRate,'
        'FlagA,AccX_A,AccY_A,AccZ_A,GyroX_A,GyroY_A,GyroZ_A,_AQ1,_AQ2,_AQ3,_AQ4,_AYawQ,_APitchQ,_ARollQ,_AYaw,_APitch,_ARoll,_Acount,_Atime,_AHS,_ADist,_AgravaccX,_AgravaccY,_AgravaccZ,_ASendRate,_ARecvRate,'
        'writeRate,rate,time' + '\n')
    init = time.time()
    while calibcounter <= 15000:
        print("Stand still for calibration")
        for sensor, location in zip(data, sockets):
            listenconcise(sensor, location)
            # print(sensor, location)
            # print(prevroll[sensor])
            # print(d[sensor][calcRoll])
            # print(nroll[sensor])
            prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
            prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
            prevpitch[sensor], d[sensor][calcPitch], npitch[sensor] = utils.correctPitch(prevpitch[sensor], d[sensor][calcPitch], npitch[sensor])
        calibAngle['rightelbowflex'] += (d[right_forearm][calcRoll] - d[right_tricep][calcRoll])
        calibAngle['rightelbowvar'] += (d[right_forearm][calcPitch] - d[right_tricep][calcPitch])
        calibAngle['rightelbowrot'] += (d[right_forearm][calcYaw] - d[right_tricep][calcYaw])
        calibAngle['leftelbowflex'] += (d[left_forearm][calcRoll] - d[left_tricep][calcRoll])
        calibAngle['leftelbowvar'] += (d[left_tricep][calcPitch] - d[left_forearm][calcPitch])
        calibAngle['leftelbowrot'] += (d[left_tricep][calcYaw] - d[left_forearm][calcYaw])
        calibcounter += 1

    for angle in calibAngle:
        calibAngle[angle] = utils.elbowcalibration(calibAngle[angle], calibcounter, angle)

    while not keyboard.is_pressed("q"):
        if counter == 0:
            cur_time = time.time()
        counter+=1
        if time.time() - cur_time > 1:
            looprate = counter / (time.time() - cur_time)
            counter = 0

        for sensor, location in zip(device_list, sockets):
            listenfordata(sensor, location)

        for sensor in device_list:
            if sensor not in [button]:
                prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
                prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
                prevpitch[sensor], d[sensor][calcPitch], npitch[sensor] = utils.correctPitch(prevpitch[sensor], d[sensor][calcPitch], npitch[sensor])

        y[0] = np.roll(y[0], -1)
        y[0][-1] = d[right_tricep][calcRoll] #Top Right

        y[1] = np.roll(y[1], -1)
        y[1][-1] = d[right_forearm][calcRoll] #Bottom Right

        y[2] = np.roll(y[2], -1)
        y[2][-1] = y[1][-1] - y[0][-1] - calibAngle['rightelbowflex']

        y[3] = np.roll(y[3], -1)
        y[3][-1] = d[right_tricep][calcPitch]

        y[4] = np.roll(y[4], -1)
        y[4][-1] = d[right_forearm][calcPitch]

        y[5] = np.roll(y[5], -1)
        y[5][-1] = y[4][-1] - y[3][-1] - calibAngle['rightelbowvar']

        y[6] = np.roll(y[6], -1)
        y[6][-1] = d[right_tricep][calcYaw]

        y[7] = np.roll(y[7], -1)
        y[7][-1] = d[right_forearm][calcYaw]

        y[8] = np.roll(y[8], -1)
        y[8][-1] = y[7][-1] - y[6][-1] - calibAngle['rightelbowrot']

        y[10] = np.roll(y[10], -1)
        y[10][-1] = d[left_tricep][calcRoll] #Top Left

        y[11] = np.roll(y[11], -1)
        y[11][-1] = d[left_forearm][calcRoll] #Bottom Left

        y[12] = np.roll(y[12], -1)
        y[12][-1] = y[11][-1] - y[10][-1] - calibAngle['leftelbowflex']

        y[13] = np.roll(y[13], -1)
        y[13][-1] = d[left_tricep][calcPitch]

        y[14] = np.roll(y[14], -1)
        y[14][-1] = d[left_forearm][calcPitch]

        y[15] = np.roll(y[15], -1)
        y[15][-1] = y[13][-1] - y[14][-1] - calibAngle['leftelbowvar'] #inverted for left

        y[16] = np.roll(y[16], -1)
        y[16][-1] = d[left_tricep][calcYaw]

        y[17] = np.roll(y[17], -1)
        y[17][-1] = d[left_forearm][calcYaw]

        y[18] = np.roll(y[18], -1)
        y[18][-1] = y[16][-1] - y[17][-1] - calibAngle['leftelbowrot'] #inverted for left

        y[9] = np.roll(y[9], -1)
        y[9][-1] = int(d[button][hs]) * 100 #heel strike button

        y[19] = np.roll(y[19], -1)
        y[19][-1] = -1 #use for ultrasonic if available

        if (flags[left_tricep] or flags[right_forearm] or flags[right_tricep] or flags[left_forearm]):
            writes +=1
            if writeCounter == 0:
                write_cur_time = time.time()
            writeCounter += 1
            if time.time() - write_cur_time > 1:
                writeRate = writeCounter / (time.time() - write_cur_time)
                writeCounter = 0
            timeWrite = time.time()-init
            file1.write(str(y[0][-1]) + ',' + str(y[1][-1]) + ',' + str(y[2][-1]) + ',' +
                        str(y[3][-1]) + ',' + str(y[4][-1]) + ',' + str(y[5][-1]) + ',' +
                        str(y[6][-1]) + ',' + str(y[7][-1]) + ',' + str(y[8][-1]) + ',' +
                        str(y[10][-1]) + ',' + str(y[11][-1]) + ',' + str(y[12][-1]) + ',' +
                        str(y[13][-1]) + ',' + str(y[14][-1]) + ',' + str(y[15][-1]) + ',' +
                        str(y[16][-1]) + ',' + str(y[17][-1]) + ',' + str(y[18][-1]) + ',' +
                        str(y[9][-1]) + ',' + str(y[19][-1]) + '\n')
            file2.write(str(flags[button]) + ',' +str(data[button]) + ',' + str(sendrate[button]) + ',' +str(rate[button]) + ',' +
                        str(flags[right_tricep]) + ',' +str(data[right_tricep]) + ',' + str(sendrate[right_tricep]) + ',' +str(rate[right_tricep]) + ',' +
                        str(flags[right_forearm]) + ',' +str(data[right_forearm]) + ',' + str(sendrate[right_forearm]) + ',' +str(rate[right_forearm]) + ',' +
                        str(flags[left_tricep]) + ',' +str(data[left_tricep]) + ',' + str(sendrate[left_tricep]) + ',' +str(rate[left_tricep]) + ',' +
                        str(flags[left_forearm]) + ',' +str(data[left_forearm]) + ',' + str(sendrate[left_forearm]) + ',' +str(rate[left_forearm]) + ',' +
                        str(writeRate) + ',' + str(rate) + ',' + str(timeWrite) + '\n')
        k = k + 1
        if k == r:
            line1.set_ydata(y[0])
            line2.set_ydata(y[1])
            line3.set_ydata(y[2])
            line4.set_ydata(y[10])
            line5.set_ydata(y[11])
            line6.set_ydata(y[12])
            # line7.set_ydata(y[6])
            # line8.set_ydata(y[7])
            line9.set_ydata(y[19])
            line10.set_ydata(y[9])
            fig.canvas.draw()
            fig.canvas.flush_events()
            k = 0

dest_path = utils.add_gait_cycle(path_gait_cycle, path_diff_pitch, joint, 1) #for button
# dest_path2 = gait.add_gait_cycle(path_gait_cycle_US, path_diff_pitch, joint, 0) #for ultrasonic