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

y = [np.zeros(display_values)] * 32

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
looprate = 0

button, buttonport = 'E', 9999
right_shank, rsport = 'D', 8888
right_thigh, rtport = 'C', 7777
right_foot, rfport = 'G', 4444
left_shank, lsport = 'N', 3333
left_thigh, ltport = 'H', 8000
left_foot, lfport = 'F', 9000
ultrasonic, ultrasonicport = 'U', 2222

# name = input("Name of patient\n")
# joint = input("Name of joint\n")
name = "Kathir"
joint = "Lower_body"
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
                prevacc[sensor], d[sensor][calcPitch], npitch[sensor] = utils.correctPitch(prevacc[sensor], d[sensor][calcPitch], d[sensor][calcPitch], npitch[sensor])

        y[0] = np.roll(y[0], -1)
        y[0][-1] = d[right_thigh][calcRoll]  # right thigh

        y[1] = np.roll(y[1], -1)
        y[1][-1] = d[right_shank][calcRoll]  # right shank

        y[2] = np.roll(y[2], -1)
        y[2][-1] = d[right_foot][calcRoll]  # right foot

        y[3] = np.roll(y[3], -1)
        y[3][-1] = y[1][-1] - y[0][-1]  # shank-thigh(right knee flexion)

        y[4] = np.roll(y[4], -1)
        y[4][-1] = y[1][-1] - y[2][-1] + calibAngle['right_shank'] - calibAngle['right_foot']  # shank-foot(right ankle flexion)

        y[5] = np.roll(y[5], -1)
        y[5][-1] = d[right_thigh][calcPitch]  # right thigh

        y[6] = np.roll(y[6], -1)
        y[6][-1] = d[right_shank][calcPitch]  # right shank

        y[7] = np.roll(y[7], -1)
        y[7][-1] = d[right_foot][calcPitch]  # right foot

        y[8] = np.roll(y[8], -1)
        y[8][-1] = y[6][-1] - y[5][-1]  # shank-thigh(right knee var-valg)

        y[9] = np.roll(y[9], -1)
        y[9][-1] = y[6][-1] - y[7][-1]  # shank-foot(right ankle 2nd axis movement)

        y[10] = np.roll(y[10], -1)
        y[10][-1] = d[right_thigh][calcYaw]  # right thigh

        y[11] = np.roll(y[11], -1)
        y[11][-1] = d[right_shank][calcYaw]  # right shank

        y[12] = np.roll(y[12], -1)
        y[12][-1] = d[right_foot][calcYaw]  # right foot

        y[13] = np.roll(y[13], -1)
        y[13][-1] = y[11][-1] - y[10][-1]  # shank-thigh(right knee rotation)

        y[14] = np.roll(y[14], -1)
        y[14][-1] = y[11][-1] - y[12][-1]  # shank-foot(right ankle 3rd axis movement)

        y[15] = np.roll(y[15], -1)
        y[15][-1] = d[left_thigh][calcRoll]  # left thigh

        y[16] = np.roll(y[16], -16)
        y[16][-1] = d[left_shank][calcRoll]  # left shank

        y[17] = np.roll(y[17], -1)
        y[17][-1] = d[left_foot][calcRoll]  # left foot

        y[18] = np.roll(y[18], -1)
        y[18][-1] = y[16][-1] - y[15][-1]  # shank-thigh(left knee flexion)

        y[19] = np.roll(y[19], -1)
        y[19][-1] = y[16][-1] - y[17][-1] + calibAngle['left_shank'] - calibAngle['left_foot']  # shank-foot(left ankle flexion)

        y[20] = np.roll(y[20], -1)
        y[20][-1] = d[left_thigh][calcPitch]  # left thigh

        y[21] = np.roll(y[21], -1)
        y[21][-1] = d[left_shank][calcPitch]  # left shank

        y[22] = np.roll(y[22], -1)
        y[22][-1] = d[left_foot][calcPitch]  # left foot

        y[23] = np.roll(y[23], -1)
        y[23][-1] = -(y[21][-1] - y[20][-1])  # -(shank-thigh)(left knee var-valg)

        y[24] = np.roll(y[24], -1)
        y[24][-1] = -(y[21][-1] - y[22][-1])  # -(shank-thigh)(left ankle 2nd axis movement)

        y[25] = np.roll(y[25], -1)
        y[25][-1] = d[left_thigh][calcYaw]  # left thigh

        y[26] = np.roll(y[26], -1)
        y[26][-1] = d[left_shank][calcYaw]  # left shank

        y[27] = np.roll(y[27], -1)
        y[27][-1] = d[left_foot][calcYaw]  # left foot

        y[28] = np.roll(y[28], -1)
        y[28][-1] = -(y[26][-1] - y[25][-1])  # -(shank-thigh)(left knee rotation)

        y[29] = np.roll(y[29], -1)
        y[29][-1] = -(y[26][-1] - y[27][-1])  # -(shank-thigh)(left ankle 3rd axis movement)

        y[30] = np.roll(y[30], -1)
        y[30][-1] = int(d[button][hs]) * 100  # button * 100

        y[31] = np.roll(y[31], -1)
        if time.time() - init < 10:
            print("Wait...")
            y[31][-1] = 0
        elif 10 <= time.time() - init < 12:
            print("StandBy...")
            y[31][-1] = 0
        else:
            print("Ready!!!!!!!!!!!!!")
            y[31][-1] = int(d[ultrasonic][hs]) * 100  # ultrasonic * 100

        if flags[left_thigh] or flags[right_thigh] or flags[right_shank] or flags[left_shank] or flags[right_foot] or flags[left_foot]:
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

dest_path = utils.add_gait_cycle(path_gait_cycle, path_diff_pitch, joint, 1)  # for button
# dest_path2 = utils.add_gait_cycle(path_gait_cycle_US, path_diff_pitch, joint, 0)  # for ultrasonic

utils.gait_cycle_mean_tester(joint, datetime.now().date(), "{}_{}_gait_cycle".format(name, trial))
