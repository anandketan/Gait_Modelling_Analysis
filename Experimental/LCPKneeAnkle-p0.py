# actual gait code

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
count_sensor = 16
timer = 17
hs = 18
dist = 19
gravaccx = 20
gravaccy = 21
gravaccz = 22

#  display_values => number of values to display at once on the plot
display_values = 500
x = np.linspace(0, display_values, display_values)

# y = [np.zeros(display_values)] * 32

y_keys = ['RightRollThigh', 'RightRollShank', 'RightRollFoot', 'RightKneeflex_angle', 'RightAnkleflex_angle',
          'RightPitchThigh', 'RightPitchShank', 'RightPitchFoot', 'RightKneevar_angle', 'RightAnklerot_angle',
          'RightYawThigh', 'RightYawShank', 'RightYawFoot', 'RightKneerot_angle', 'RightAnklefootprog_angle',
          'LeftRollThigh', 'LeftRollShank', 'LeftRollFoot', 'LeftKneeflex_angle', 'LeftAnkleflex_angle',
          'LeftPitchThigh', 'LeftPitchShank', 'LeftPitchFoot', 'LeftKneevar_angle', 'LeftAnklerot_angle',
          'LeftYawThigh', 'LeftYawShank', 'LeftYawFoot', 'LeftKneerot_angle', 'LeftAnklefootprog_angle',
          'hs', 'hs_US']
y = {xx: [np.zeros(display_values)] for xx in y_keys}

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-500, 500])
line1, = ax.plot(x, y['RightRollThigh'][0], 'b-', label='roll')
line2, = ax.plot(x, y['RightRollShank'][0], 'r-', label='pitch')
line3, = ax.plot(x, y['RightRollFoot'][0], 'y-', label='yaw')
# line4, = ax.plot(x, y['RightKneeflex_angle'][0], 'g-', label='pitchCdirect')
# line5, = ax.plot(x, y['RightAnkleflex_angle'][0], 'm-', label='pitchBdirect')
# line6, = ax.plot(x, y['RightPitchThigh'][0], 'k-', label='nC')
# line7, = ax.plot(x, y['RightPitchShank'][0], 'c-', label='accZ-C')
# line8, = ax.plot(x, y['RightPitchFoot'][0], 'tab:pink', label='nB')
# line9, = ax.plot(x, y['RightKneevar_angle'][0], 'tab:gray', label='accZ-B')
line10, = ax.plot(x, y['hs'][0], 'tab:brown', label='hs')
line11, = ax.plot(x, y['hs_US'][0], 'tab:pink', label='hs_US')
ax.legend()
# figManager = plt.get_current_fig_manager()
# figManager.window.showMaximized()
#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 50
counter = 0
k = 0
looprate = 0

button, buttonport = 'E', 9999
right_shank, rsport = 'D', 8888
right_thigh, rtport = 'C', 7777
right_foot, rfport = 'N', 3333
left_shank, lsport = 'F', 9000
left_thigh, ltport = 'H', 8000
left_foot, lfport = 'B', 6666
ultrasonic, ultrasonicport = 'U', 2222

# name = input("Name of patient\n")
# joint = input("Name of joint\n")
name = "Test"
joint = "Test"
trial = input("Trial number?\n")
file_name_all = '{}_{}_allSensorData_{}_{}_{}_{}.csv'.format(name,
                                                             trial,
                                                             datetime.now().date(),
                                                             datetime.now().time().hour,
                                                             datetime.now().time().minute,
                                                             datetime.now().time().second)
file_name_diff_pitch = 'diff_pitch_{}_{}.csv'.format(name, trial)
file_name_gait_cycle = '{}_{}_gait_cycle.csv'.format(name, trial)
file_name_gait_cycle_US = '{}_{}_gait_cycle_US.csv'.format(name, trial)
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir,
                        'DataFolder',
                        '{}'.format(joint),
                        '{}'.format(datetime.now().date()),
                        '{}_{}_gait_cycle'.format(name, trial))
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
calibAngle = {'right_shank': 0, 'right_foot': 0, 'left_shank': 0, 'left_foot': 0}

joint_device = {'button': button, 'right_shank': right_shank, 'right_thigh': right_thigh, 'right_foot': right_foot,
                'left_shank': left_shank, 'left_thigh': left_thigh, 'left_foot': left_foot, 'ultrasonic': ultrasonic}

device_list = [button, right_shank, right_thigh, left_thigh, ultrasonic, right_foot, left_shank, left_foot]
port_list = [buttonport, rsport, rtport, ltport, ultrasonicport, rfport, lsport, lfport]

prevdata = {}
data = {}
d = {}

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
    if device != button:
        data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        prevdata[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
    else:
        data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        prevdata[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(8)]
for port, sock in zip(port_list, sock_list):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    sock.setblocking(0)

socks = {}
for device, sock in zip(device_list, sock_list):
    socks[device] = sock

sockets = {'button': socks[button], 'right_shank': socks[right_shank], 'right_thigh': socks[right_thigh],
           'left_thigh': socks[left_thigh], 'ultrasonic': socks[ultrasonic], 'right_foot': socks[right_foot],
           'left_shank': socks[left_shank], 'left_foot': socks[left_foot]}

with open(os.path.join(dest_dir, 'device_list.txt'), 'w') as f:
    f.write(str(device_list) + '\n')
    f.write(str(port_list) + '\n')
    # f.write(str(sockets) + '\n')
    f.write(str(joint_device) + '\n')
    f.write('Storage order: {}{}{}{}{}{}{}{}\n'.format(button, right_shank, right_thigh, left_thigh, ultrasonic,
                                                       right_foot, left_shank, left_foot))

with open(path_diff_pitch, 'w') as file1, open(path_all, 'w') as file2:
    file1.write('RightRollThigh,RightRollShank,RightRollFoot,RightKneeflex_angle,RightAnkleflex_angle,'
                'RightPitchThigh,RightPitchShank,RightPitchFoot,RightKneevar_angle,RightAnklerot_angle,'
                'RightYawThigh,RightYawShank,RightYawFoot,RightKneerot_angle,RightAnklefootprog_angle,'
                'LeftRollThigh,LeftRollShank,LeftRollFoot,LeftKneeflex_angle,LeftAnkleflex_angle,'
                'LeftPitchThigh,LeftPitchShank,LeftPitchFoot,LeftKneevar_angle,LeftAnklerot_angle,'
                'LeftYawThigh,LeftYawShank,LeftYawFoot,LeftKneerot_angle,LeftAnklefootprog_angle,'
                'hs,hs_US\n')
    file2.write(
        'FlagE,AccX_E,AccY_E,AccZ_E,GyroX_E,GyroY_E,GyroZ_E,_EQ1,_EQ2,_EQ3,_EQ4,_EYawQ,_EPitchQ,_ERollQ,_EYaw,_EPitch,_ERoll,_Ecount,_Etime,_EStep,_EDist,_ESendRate,_ERecvRate,'
        'FlagD,AccX_D,AccY_D,AccZ_D,GyroX_D,GyroY_D,GyroZ_D,_DQ1,_DQ2,_DQ3,_DQ4,_DYawQ,_DPitchQ,_DRollQ,_DYaw,_DPitch,_DRoll,_Dcount,_Dtime,_DHS,_DDist,_DgravaccX,_DgravaccY,_DgravaccZ,_DSendRate,_DRecvRate,'
        'FlagC,AccX_C,AccY_C,AccZ_C,GyroX_C,GyroY_C,GyroZ_C,_CQ1,_CQ2,_CQ3,_CQ4,_CYawQ,_CPitchQ,_CRollQ,_CYaw,_CPitch,_CRoll,_Ccount,_Ctime,_CHS,_CDist,_CgravaccX,_CgravaccY,_CgravaccZ,_CSendRate,_CRecvRate,'
        'FlagB,AccX_B,AccY_B,AccZ_B,GyroX_B,GyroY_B,GyroZ_B,_BQ1,_BQ2,_BQ3,_BQ4,_BYawQ,_BPitchQ,_BRollQ,_BYaw,_BPitch,_BRoll,_Bcount,_Btime,_BHS,_BDist,_BgravaccX,_BgravaccY,_BgravaccZ,_BSendRate,_BRecvRate,'
        'FlagA,AccX_A,AccY_A,AccZ_A,GyroX_A,GyroY_A,GyroZ_A,_AQ1,_AQ2,_AQ3,_AQ4,_AYawQ,_APitchQ,_ARollQ,_AYaw,_APitch,_ARoll,_Acount,_Atime,_AHS,_ADist,_AgravaccX,_AgravaccY,_AgravaccZ,_ASendRate,_ARecvRate,'
        'FlagG,AccX_G,AccY_G,AccZ_G,GyroX_G,GyroY_G,GyroZ_G,_GQ1,_GQ2,_GQ3,_GQ4,_GYawQ,_GPitchQ,_GRollQ,_GYaw,_GPitch,_GRoll,_Gcount,_Gtime,_GHS,_GDist,_GgravaccX,_GgravaccY,_GgravaccZ,_GSendRate,_GRecvRate,'
        'FlagN,AccX_N,AccY_N,AccZ_N,GyroX_N,GyroY_N,GyroZ_N,_NQ1,_NQ2,_NQ3,_NQ4,_NYawQ,_NPitchQ,_NRollQ,_NYaw,_NPitch,_NRoll,_Ncount,_Ntime,_NHS,_NDist,_NgravaccX,_NgravaccY,_NgravaccZ,_NSendRate,_NRecvRate,'
        'FlagF,AccX_F,AccY_F,AccZ_F,GyroX_F,GyroY_F,GyroZ_F,_FQ1,_FQ2,_FQ3,_FQ4,_FYawQ,_FPitchQ,_FRollQ,_FYaw,_FPitch,_FRoll,_Fcount,_Ftime,_FHS,_FDist,_FgravaccX,_FgravaccY,_FgravaccZ,_FSendRate,_FRecvRate,'
        'writeRate,rate,time' + '\n')
    init = time.time()
    while calibcounter <= 15000:
        for sensor, location in zip(data, sockets):
            if location in calibAngle:
                listenconcise(sensor, location)
                prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
                calibAngle[location] += d[sensor][calcRoll]
        
        calibcounter += 1

    for location in calibAngle:
        calibAngle[location] = utils.anklecalibration(calibAngle[location], calibcounter, location.split('_')[0], location.split('_')[1])

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
            if sensor not in [button, ultrasonic]:
                prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = utils.correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
                prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = utils.correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
                # prevacc[sensor], d[sensor][calcPitch], npitch[sensor] = utils.correctPitch(prevacc[sensor], d[sensor][calcPitch], d[sensor][calcPitch], npitch[sensor])

        y['RightRollThigh'][0] = np.roll(y['RightRollThigh'][0], -1)
        y['RightRollThigh'][0][-1] = d[right_thigh][calcRoll]  # right thigh

        y['RightRollShank'][0] = np.roll(y['RightRollShank'][0], -1)
        y['RightRollShank'][0][-1] = d[right_shank][calcRoll]  # right shank

        y['RightRollFoot'][0] = np.roll(y['RightRollFoot'][0], -1)
        y['RightRollFoot'][0][-1] = d[right_foot][calcRoll]  # right foot

        y['RightKneeflex_angle'][0] = np.roll(y['RightKneeflex_angle'][0], -1)
        y['RightKneeflex_angle'][0][-1] = y['RightRollShank'][0][-1] - y['RightRollThigh'][0][
            -1]  # shank-thigh(right knee flexion)

        y['RightAnkleflex_angle'][0] = np.roll(y['RightAnkleflex_angle'][0], -1)
        y['RightAnkleflex_angle'][0][-1] = y['RightRollShank'][0][-1] - y['RightRollFoot'][0][-1] + calibAngle[
            'right_shank'] - calibAngle['right_foot']  # shank-foot(right ankle flexion)

        y['RightPitchThigh'][0] = np.roll(y['RightPitchThigh'][0], -1)
        y['RightPitchThigh'][0][-1] = d[right_thigh][calcPitch]  # right thigh

        y['RightPitchShank'][0] = np.roll(y['RightPitchShank'][0], -1)
        y['RightPitchShank'][0][-1] = d[right_shank][calcPitch]  # right shank

        y['RightPitchFoot'][0] = np.roll(y['RightPitchFoot'][0], -1)
        y['RightPitchFoot'][0][-1] = d[right_foot][calcPitch]  # right foot

        y['RightKneevar_angle'][0] = np.roll(y['RightKneevar_angle'][0], -1)
        y['RightKneevar_angle'][0][-1] = y['RightPitchShank'][0][-1] - y['RightPitchThigh'][0][
            -1]  # shank-thigh(right knee var-valg)

        y['RightAnklerot_angle'][0] = np.roll(y['RightAnklerot_angle'][0], -1)
        y['RightAnklerot_angle'][0][-1] = y['RightPitchShank'][0][-1] - y['RightPitchFoot'][0][
            -1]  # shank-foot(right ankle 2nd axis movement)

        y['RightYawThigh'][0] = np.roll(y['RightYawThigh'][0], -1)
        y['RightYawThigh'][0][-1] = d[right_thigh][calcYaw]  # right thigh

        y['RightYawShank'][0] = np.roll(y['RightYawShank'][0], -1)
        y['RightYawShank'][0][-1] = d[right_shank][calcYaw]  # right shank

        y['RightYawFoot'][0] = np.roll(y['RightYawFoot'][0], -1)
        y['RightYawFoot'][0][-1] = d[right_foot][calcYaw]  # right foot

        y['RightKneerot_angle'][0] = np.roll(y['RightKneerot_angle'][0], -1)
        y['RightKneerot_angle'][0][-1] = y['RightYawShank'][0][-1] - y['RightYawThigh'][0][
            -1]  # shank-thigh(right knee rotation)

        y['RightAnklefootprog_angle'][0] = np.roll(y['RightAnklefootprog_angle'][0], -1)
        y['RightAnklefootprog_angle'][0][-1] = y['RightYawShank'][0][-1] - y['RightYawFoot'][0][
            -1]  # shank-foot(right ankle 3rd axis movement)

        y['LeftRollThigh'][0] = np.roll(y['LeftRollThigh'][0], -1)
        y['LeftRollThigh'][0][-1] = d[left_thigh][calcRoll]  # left thigh

        y['LeftRollShank'][0] = np.roll(y['LeftRollShank'][0], -1)
        y['LeftRollShank'][0][-1] = d[left_shank][calcRoll]  # left shank

        y['LeftRollFoot'][0] = np.roll(y['LeftRollFoot'][0], -1)
        y['LeftRollFoot'][0][-1] = d[left_foot][calcRoll]  # left foot

        y['LeftKneeflex_angle'][0] = np.roll(y['LeftKneeflex_angle'][0], -1)
        y['LeftKneeflex_angle'][0][-1] = y['LeftRollShank'][0][-1] - y['LeftRollThigh'][0][
            -1]  # shank-thigh(left knee flexion)

        y['LeftAnkleflex_angle'][0] = np.roll(y['LeftAnkleflex_angle'][0], -1)
        y['LeftAnkleflex_angle'][0][-1] = y['LeftRollShank'][0][-1] - y['LeftRollFoot'][0][-1] + calibAngle[
            'left_shank'] - calibAngle['left_foot']  # shank-foot(left ankle flexion)

        y['LeftPitchThigh'][0] = np.roll(y['LeftPitchThigh'][0], -1)
        y['LeftPitchThigh'][0][-1] = d[left_thigh][calcPitch]  # left thigh

        y['LeftPitchShank'][0] = np.roll(y['LeftPitchShank'][0], -1)
        y['LeftPitchShank'][0][-1] = d[left_shank][calcPitch]  # left shank

        y['LeftPitchFoot'][0] = np.roll(y['LeftPitchFoot'][0], -1)
        y['LeftPitchFoot'][0][-1] = d[left_foot][calcPitch]  # left foot

        y['LeftKneevar_angle'][0] = np.roll(y['LeftKneevar_angle'][0], -1)
        y['LeftKneevar_angle'][0][-1] = -(
                    y['LeftPitchShank'][0][-1] - y['LeftPitchThigh'][0][-1])  # -(shank-thigh)(left knee var-valg)

        y['LeftAnklerot_angle'][0] = np.roll(y['LeftAnklerot_angle'][0], -1)
        y['LeftAnklerot_angle'][0][-1] = -(y['LeftPitchShank'][0][-1] - y['LeftPitchFoot'][0][
            -1])  # -(shank-thigh)(left ankle 2nd axis movement)

        y['LeftYawThigh'][0] = np.roll(y['LeftYawThigh'][0], -1)
        y['LeftYawThigh'][0][-1] = d[left_thigh][calcYaw]  # left thigh

        y['LeftYawShank'][0] = np.roll(y['LeftYawShank'][0], -1)
        y['LeftYawShank'][0][-1] = d[left_shank][calcYaw]  # left shank

        y['LeftYawFoot'][0] = np.roll(y['LeftYawFoot'][0], -1)
        y['LeftYawFoot'][0][-1] = d[left_foot][calcYaw]  # left foot

        y['LeftKneerot_angle'][0] = np.roll(y['LeftKneerot_angle'][0], -1)
        y['LeftKneerot_angle'][0][-1] = -(
                    y['LeftYawShank'][0][-1] - y['LeftYawThigh'][0][-1])  # -(shank-thigh)(left knee rotation)

        y['LeftAnklefootprog_angle'][0] = np.roll(y['LeftAnklefootprog_angle'][0], -1)
        y['LeftAnklefootprog_angle'][0][-1] = -(
                    y['LeftYawShank'][0][-1] - y['LeftYawFoot'][0][-1])  # -(shank-thigh)(left ankle 3rd axis movement)

        y['hs'][0] = np.roll(y['hs'][0], -1)
        y['hs'][0][-1] = int(d[button][hs]) * 100  # button * 100

        y['hs_US'][0] = np.roll(y['hs_US'][0], -1)
        if time.time() - init < 10:
            print("Wait...")
            y['hs_US'][0][-1] = 0
        elif 10 <= time.time() - init < 12:
            print("StandBy...")
            y['hs_US'][0][-1] = 0
        else:
            print("Ready!!!!!!!!!!!!!")
            y['hs_US'][0][-1] = int(d[ultrasonic][hs]) * 100  # ultrasonic * 100

        if flags[left_thigh] or flags[right_thigh] or flags[right_shank] or flags[left_shank] or flags[right_foot] or \
                flags[left_foot]:
            writes += 1
            if writeCounter == 0:
                write_cur_time = time.time()
            writeCounter += 1
            if time.time() - write_cur_time > 1:
                writeRate = writeCounter / (time.time() - write_cur_time)
                writeCounter = 0
            timeWrite = time.time() - init

            file1.write(str(y['RightRollThigh'][0][-1]) + ',' + str(y['RightRollShank'][0][-1]) + ',' + str(y['RightRollFoot'][0][-1]) + ',' + str(y['RightKneeflex_angle'][0][-1]) + ',' + str(y['RightAnkleflex_angle'][0][-1]) + ',' +
                        str(y['RightPitchThigh'][0][-1]) + ',' + str(y['RightPitchShank'][0][-1]) + ',' + str(y['RightPitchFoot'][0][-1]) + ',' + str(y['RightKneevar_angle'][0][-1]) + ',' + str(y['RightAnklerot_angle'][0][-1]) + ',' +
                        str(y['RightYawThigh'][0][-1]) + ',' + str(y['RightYawShank'][0][-1]) + ',' + str(y['RightYawFoot'][0][-1]) + ',' + str(y['RightKneerot_angle'][0][-1]) + ',' + str(y['RightAnklefootprog_angle'][0][-1]) + ',' +
                        str(y['LeftRollThigh'][0][-1]) + ',' + str(y['LeftRollShank'][0][-1]) + ',' + str(y['LeftRollFoot'][0][-1]) + ',' + str(y['LeftKneeflex_angle'][0][-1]) + ',' + str(y['LeftAnkleflex_angle'][0][-1]) + ',' +
                        str(y['LeftPitchThigh'][0][-1]) + ',' + str(y['LeftPitchShank'][0][-1]) + ',' + str(y['LeftPitchFoot'][0][-1]) + ',' + str(y['LeftKneevar_angle'][0][-1]) + ',' + str(y['LeftAnklerot_angle'][0][-1]) + ',' +
                        str(y['LeftYawThigh'][0][-1]) + ',' + str(y['LeftYawShank'][0][-1]) + ',' + str(y['LeftYawFoot'][0][-1]) + ',' + str(y['LeftKneerot_angle'][0][-1]) + ',' + str(y['LeftAnklefootprog_angle'][0][-1]) + ',' +
                        str(y['hs'][0][-1]) + ',' + str(y['hs_US'][0][-1]) + '\n')
            file2.write(str(flags[button]) + ',' + str(data[button]) + ',' + str(sendrate[button]) + ',' + str(rate[button]) + ',' +
                        str(flags[right_shank]) + ',' + str(data[right_shank]) + ',' + str(sendrate[right_shank]) + ',' + str(rate[right_shank]) + ',' +
                        str(flags[right_thigh]) + ',' + str(data[right_thigh]) + ',' + str(sendrate[right_thigh]) + ',' + str(rate[right_thigh]) + ',' +
                        str(flags[left_thigh]) + ',' + str(data[left_thigh]) + ',' + str(sendrate[left_thigh]) + ',' + str(rate[left_thigh]) + ',' +
                        str(flags[ultrasonic]) + ',' + str(data[ultrasonic]) + ',' + str(sendrate[ultrasonic]) + ',' + str(rate[ultrasonic]) + ',' +
                        str(flags[right_foot]) + ',' + str(data[right_foot]) + ',' + str(sendrate[right_foot]) + ',' + str(rate[right_foot]) + ',' +
                        str(flags[left_shank]) + ',' + str(data[left_shank]) + ',' + str(sendrate[left_shank]) + ',' + str(rate[left_shank]) + ',' +
                        str(flags[left_foot]) + ',' + str(data[left_foot]) + ',' + str(sendrate[left_foot]) + ',' + str(rate[left_foot]) + ',' +
                        str(writeRate) + ',' + str(looprate) + ',' + str(time.time()) + '\n')
        k = k + 1
        # count += 1
        # print("Data looprate=",looprate)
        if k == r:
            # right shank, thigh roll, F/E of knee
            line1.set_ydata(y['RightRollShank'])
            line2.set_ydata(y['RightPitchShank'])
            line3.set_ydata(y['RightYawShank'])

            # right knee F/E, V/V, Rot
            # line1.set_ydata(y['RightKneeflex_angle'][0])
            # line2.set_ydata(y['RightKneevar_angle'][0])
            # line3.set_ydata(y['RightKneerot_angle'][0])

            # left knee F/E, V/V, Rot
            # line1.set_ydata(y['LeftKneeflex_angle'][0])
            # line2.set_ydata(y['LeftKneevar_angle'][0])
            # line3.set_ydata(y['LeftKneerot_angle'][0])

            # right ankle F/E, pitchdiff, yawdiff
            # line1.set_ydata(y['RightAnkleflex_angle'][0])
            # line2.set_ydata(y['RightAnklerot_angle'][0])
            # line3.set_ydata(y['RightAnklefootprog_angle'][0])

            # left ankle F/E, pitchdiff, yawdiff
            # line1.set_ydata(y['LeftAnkleflex_angle'][0])
            # line2.set_ydata(y['LeftAnklerot_angle'][0])
            # line3.set_ydata(y['LeftAnklefootprog_angle'][0])

            line10.set_ydata(y['hs'])
            line11.set_ydata(y['hs_US'])
            fig.canvas.draw()
            fig.canvas.flush_events()
            k = 0

dest_path = utils.add_gait_cycle(path_gait_cycle, path_diff_pitch, joint, 1)  # for button
# dest_path2 = utils.add_gait_cycle(path_gait_cycle_US, path_diff_pitch, joint, 0)  # for ultrasonic

utils.gait_cycle_mean_tester(joint, str(datetime.now().date()), "{}_{}_gait_cycle".format(name, trial))
