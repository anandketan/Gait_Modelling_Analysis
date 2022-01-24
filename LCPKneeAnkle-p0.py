import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import math
import datetime
from datetime import datetime
import os
import keyboard
import pressure_sensor_gait_cycle as gait


def correctYaw(prev_yaw, yaw, n):
    if prev_yaw >= 160 and prev_yaw <= 180 and float(yaw) >= -180 and float(yaw) <= -160:
        n += 1
    elif float(yaw) >= 160 and float(yaw) <= 180 and prev_yaw >= -180 and prev_yaw <= -160:
        n -= 1

    prevyawnew = float(yaw)
    # print(nC, pitch, prevaccC, d['C'][az])
    yawnew = n * 360 + float(yaw)
    return prevyawnew, yawnew, n


def correctRoll(prev_roll, roll, n):
    if prev_roll >= 160 and prev_roll <= 180 and float(roll) >= -180 and float(roll) <= -160:
        n += 1
    elif float(roll) >= 160 and float(roll) <= 180 and prev_roll >= -180 and prev_roll <= -160:
        n -= 1

    prevrollnew = float(roll)
    # print(nC, pitch, prevaccC, d['C'][az])
    rollnew = n * 360 + float(roll)
    return prevrollnew, rollnew, n


def correctPitch(prev_pitch, pitch, n):
    prevpitchnew = float(pitch)
    pitchnew = float(pitch)
    return prevpitchnew, pitchnew, n


def anklecalibration(anglesum, calibrationcounter, side, segment):
    calibAngle = anglesum/calibrationcounter
    print("Initial {} {} angle:".format(side, segment), calibAngle)
    calibAngle = -180 - calibAngle
    print("{} {} calibration angle:".format(side, segment), calibAngle)
    return calibAngle


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

prevdata = {'E': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'D': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'C': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0",
            'B': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'A': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'G': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0",
            'N': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'F': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"}

data = {'E': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'D': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'C': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0",
        'B': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'A': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'G': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0",
        'N': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0", 'F': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"}

d = {'E': [], 'D': [], 'C': [], 'B': [], 'A': [], 'G': [], 'N': [], 'F': []}

#  display_values => number of values to display at once on the plot
display_values = 500
x = np.linspace(0, display_values, display_values)

y = [np.zeros(display_values)]*32

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-500, 500])
line1, = ax.plot(x, y[0], 'b-', label='rollFoot')
line2, = ax.plot(x, y[1], 'r-', label='rollAnkle')
line3, = ax.plot(x, y[2], 'y-', label='flexangle')
# line4, = ax.plot(x, y[3], 'g-', label='pitchCdirect')
# line5, = ax.plot(x, y[4], 'm-', label='pitchBdirect')
# line6, = ax.plot(x, y[5], 'k-', label='nC')
# line7, = ax.plot(x, y[6], 'c-', label='accZ-C')
# line8, = ax.plot(x, y[7], 'tab:pink', label='nB')
# line9, = ax.plot(x, y[8], 'tab:gray', label='accZ-B')
line10, = ax.plot(x, y[9], 'tab:brown', label='hs')
line11, = ax.plot(x, y[10], 'tab:pink', label='hs_US')
ax.legend()
# figManager = plt.get_current_fig_manager()
# figManager.window.showMaximized()
#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 50
counter = 0
k = 0
rate = 0

prevyaw = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}
nyaw = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}

prevroll = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}
nroll = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}

prevpitch = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}
npitch = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}

# name = input("Name of patient\n")
# joint = input("Name of joint\n")
name = "Test"
joint = "Lower_body"
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

flags = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}
count = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}
initialtime = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}
rate = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}
sendrate = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}
sendinitialtime = {'E': 0, 'D': 0, 'C': 0, 'B': 0, 'A': 0, 'G': 0, 'N': 0, 'F': 0}

writeCounter = 0
writeRate = 0
writes = 0

calibcounter = 0
calibAngle = {'right_shank': 0, 'right_foot': 0, 'left_shank': 0, 'left_foot': 0}

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # button --> E
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0", 9999))
s1.setblocking(0)

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # right shank --> D
s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s2.bind(("0.0.0.0", 8888))
s2.setblocking(0)

s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # right thigh --> C
s3.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s3.bind(("0.0.0.0", 7777))
s3.setblocking(0)

s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # left thigh --> B
s4.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s4.bind(("0.0.0.0", 6666))
s4.setblocking(0)

s5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # ultrasonic --> A
s5.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s5.bind(("0.0.0.0", 5555))
s5.setblocking(0)

s6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # right foot --> G
s6.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s6.bind(("0.0.0.0", 4444))
s6.setblocking(0)

s7 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # left shank --> N
s7.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s7.bind(("0.0.0.0", 3333))
s7.setblocking(0)

s8 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # left foot --> F
s8.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s8.bind(("0.0.0.0", 9000))
s8.setblocking(0)

sockets = {'button': s1, 'right_shank': s2, 'right_thigh': s3, 'left_thigh': s4, 'ultrasonic': s5, 'right_foot': s6, 'left_shank': s7, 'left_foot': s8}

with open(path_diff_pitch, 'w') as file1, open(path_all, 'w') as file2:
    file1.write('RightRollThigh,RightRollShank,RightRollFoot,RightKneeflex_angle,RightAnkleflex_angle,'
                'RightPitchThigh,RightPitchShank,RightPitchFoot,RightKneevar_angle,RightAnkleabd_angle,'
                'RightYawThigh,RightYawShank,RightYawFoot,RightKneerot_angle,RightAnklerot_angle,'
                'LeftRollThigh,LeftRollShank,LeftRollFoot,LeftKneeflex_angle,LeftAnkleflex_angle,'
                'LeftPitchThigh,LeftPitchShank,LeftPitchFoot,LeftKneevar_angle,LeftAnkleabd_angle,'
                'LeftYawThigh,LeftYawShank,LeftYawFoot,LeftKneerot_angle,LeftAnklerot_angle,'
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
                prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
                calibAngle[location] += d[sensor][calcRoll]
        
        calibcounter += 1

    for location in calibAngle:
        calibAngle[location] = anklecalibration(calibAngle[location], calibcounter, location.split('_')[0], location.split('_')[1])

    while not keyboard.is_pressed("q"):
        if counter == 0:
            cur_time = time.time()
        counter += 1
        if time.time() - cur_time > 1:
            rate = counter / (time.time() - cur_time)
            counter = 0
            
        for sensor, location in zip(data, sockets):
            listenfordata(sensor, location)
            
        for sensor in data:
            if sensor not in ['E', 'A']:
                prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor] = correctYaw(prevyaw[sensor], d[sensor][calcYaw], nyaw[sensor])
                prevroll[sensor], d[sensor][calcRoll], nroll[sensor] = correctRoll(prevroll[sensor], d[sensor][calcRoll], nroll[sensor])
                prevpitch[sensor], d[sensor][calcPitch], npitch[sensor] = correctPitch(prevpitch[sensor], d[sensor][calcPitch], npitch[sensor])

        y[0] = np.roll(y[0], -1)
        y[0][-1] = d['C'][calcRoll]  # right thigh

        y[1] = np.roll(y[1], -1)
        y[1][-1] = d['D'][calcRoll]  # right shank

        y[2] = np.roll(y[2], -1)
        y[2][-1] = d['G'][calcRoll]  # right foot

        y[3] = np.roll(y[3], -1)
        y[3][-1] = y[1][-1] - y[0][-1]

        y[4] = np.roll(y[4], -1)
        y[4][-1] = y[1][-1] - y[2][-1] + calibAngle['right_shank'] - calibAngle['right_foot']

        y[5] = np.roll(y[5], -1)
        y[5][-1] = d['C'][calcPitch]  # right thigh

        y[6] = np.roll(y[6], -1)
        y[6][-1] = d['D'][calcPitch]  # right shank

        y[7] = np.roll(y[7], -1)
        y[7][-1] = d['G'][calcPitch]  # right foot

        y[8] = np.roll(y[8], -1)
        y[8][-1] = y[6][-1] - y[5][-1]

        y[9] = np.roll(y[9], -1)
        y[9][-1] = y[6][-1] - y[7][-1]

        y[10] = np.roll(y[10], -1)
        y[10][-1] = d['C'][calcYaw]  # right thigh

        y[11] = np.roll(y[11], -1)
        y[11][-1] = d['D'][calcYaw]  # right shank

        y[12] = np.roll(y[12], -1)
        y[12][-1] = d['G'][calcYaw]  # right foot

        y[13] = np.roll(y[13], -1)
        y[13][-1] = y[11][-1] - y[10][-1]

        y[14] = np.roll(y[14], -1)
        y[14][-1] = y[11][-1] - y[12][-1]

        y[15] = np.roll(y[15], -1)
        y[15][-1] = d['C'][calcRoll]  # right thigh

        y[16] = np.roll(y[16], -16)
        y[16][-1] = d['D'][calcRoll]  # right shank

        y[17] = np.roll(y[17], -1)
        y[17][-1] = d['G'][calcRoll]  # right foot

        y[18] = np.roll(y[18], -1)
        y[18][-1] = y[16][-1] - y[15][-1]

        y[19] = np.roll(y[19], -1)
        y[19][-1] = y[16][-1] - y[17][-1] + calibAngle['left_shank'] - calibAngle['left_foot']

        y[20] = np.roll(y[20], -1)
        y[20][-1] = d['C'][calcPitch]  # left thigh

        y[21] = np.roll(y[21], -1)
        y[21][-1] = d['D'][calcPitch]  # left shank

        y[22] = np.roll(y[22], -1)
        y[22][-1] = d['G'][calcPitch]  # left foot

        y[23] = np.roll(y[23], -1)
        y[23][-1] = -(y[21][-1] - y[20][-1])

        y[24] = np.roll(y[24], -1)
        y[24][-1] = -(y[21][-1] - y[22][-1])

        y[25] = np.roll(y[25], -1)
        y[25][-1] = d['C'][calcYaw]  # left thigh

        y[26] = np.roll(y[26], -1)
        y[26][-1] = d['D'][calcYaw]  # left shank

        y[27] = np.roll(y[27], -1)
        y[27][-1] = d['G'][calcYaw]  # left foot

        y[28] = np.roll(y[28], -1)
        y[28][-1] = -(y[26][-1] - y[25][-1])

        y[29] = np.roll(y[29], -1)
        y[29][-1] = -(y[26][-1] - y[27][-1])

        y[30] = np.roll(y[30], -1)
        y[30][-1] = int(d['E'][hs]) * 100

        y[31] = np.roll(y[31], -1)
        if time.time() - init < 10:
            print("Wait...")
            y[31][-1] = 0
        else:
            print("Ready!!!!!!!!!!!!!")
            y[31][-1] = int(d['A'][hs]) * 100

        if flags['B'] or flags['C'] or flags['D'] or flags['N'] or flags['G'] or flags['F']:
            writes += 1
            if writeCounter == 0:
                write_cur_time = time.time()
            writeCounter += 1
            if time.time() - write_cur_time > 1:
                writeRate = writeCounter / (time.time() - write_cur_time)
                writeCounter = 0
            timeWrite = time.time()-init
            
            file1.write(str(y[0][-1]) + ',' + str(y[1][-1]) + ',' + str(y[2][-1]) + ',' + str(y[3][-1]) + ',' + str(y[4][-1]) + ',' +
                        str(y[5][-1]) + ',' + str(y[6][-1]) + ',' + str(y[7][-1]) + ',' + str(y[8][-1]) + ',' + str(y[9][-1]) + ',' +
                        str(y[10][-1]) + ',' + str(y[11][-1]) + ',' + str(y[12][-1]) + ',' + str(y[13][-1]) + ',' + str(y[14][-1]) + ',' +
                        str(y[15][-1]) + ',' + str(y[16][-1]) + ',' + str(y[17][-1]) + ',' + str(y[18][-1]) + ',' + str(y[19][-1]) + ',' +
                        str(y[20][-1]) + ',' + str(y[21][-1]) + ',' + str(y[22][-1]) + ',' + str(y[23][-1]) + ',' + str(y[24][-1]) + ',' +
                        str(y[25][-1]) + ',' + str(y[26][-1]) + ',' + str(y[27][-1]) + ',' + str(y[28][-1]) + ',' + str(y[29][-1]) + ',' +
                        str(y[30][-1]) + ',' + str(y[31][-1]) + '\n')
            file2.write(str(flags['E']) + ',' + str(data['E']) + ',' + str(sendrate['E']) + ',' + str(rate['E']) + ',' +
                        str(flags['D']) + ',' + str(data['D']) + ',' + str(sendrate['D']) + ',' + str(rate['D']) + ',' +
                        str(flags['C']) + ',' + str(data['C']) + ',' + str(sendrate['C']) + ',' + str(rate['C']) + ',' +
                        str(flags['B']) + ',' + str(data['B']) + ',' + str(sendrate['B']) + ',' + str(rate['B']) + ',' +
                        str(flags['A']) + ',' + str(data['A']) + ',' + str(sendrate['A']) + ',' + str(rate['A']) + ',' +
                        str(flags['G']) + ',' + str(data['G']) + ',' + str(sendrate['G']) + ',' + str(rate['G']) + ',' +
                        str(flags['N']) + ',' + str(data['N']) + ',' + str(sendrate['N']) + ',' + str(rate['N']) + ',' +
                        str(flags['F']) + ',' + str(data['F']) + ',' + str(sendrate['F']) + ',' + str(rate['F']) + ',' +
                        str(writeRate) + ',' + str(rate) + ',' + str(time.time()) + '\n')
        k = k + 1
        # count += 1
        # print("Data rate=",rate)
        if k == r:
            line1.set_ydata(y[0])
            line2.set_ydata(y[1])
            line3.set_ydata(y[2])
            # line1.set_ydata(y4)
            # line2.set_ydata(y5)
            # line3.set_ydata(y6)
            # line1.set_ydata(y7)
            # line2.set_ydata(y8)
            # line3.set_ydata(y9)
            line10.set_ydata(y[30])
            line11.set_ydata(y[31])
            fig.canvas.draw()
            fig.canvas.flush_events()
            k = 0

dest_path = gait.add_gait_cycle(path_gait_cycle, path_diff_pitch, joint, 1)  # for button
dest_path2 = gait.add_gait_cycle(path_gait_cycle_US, path_diff_pitch, joint, 0)  # for ultrasonic
