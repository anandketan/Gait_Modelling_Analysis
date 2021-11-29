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

# def correctPitch(prevacc, gravZ, pitch, n):
#     if prevacc > 0 and float(gravZ) <= 0 and float(pitch) > 0:
#         n -= 1
#     elif prevacc > 0 and float(gravZ) <= 0 and float(pitch) < 0:
#         n += 1
#     elif prevacc <= 0 and float(gravZ) > 0 and float(pitch) > 0:
#         n += 1
#     elif prevacc <= 0 and float(gravZ) > 0 and float(pitch) < 0:
#         n -= 1
#
#     prevaccNew = float(gravZ)
#     # print(nC, pitch, prevaccC, d3[az])
#     pitchNew = n * 180 + math.pow(-1, n) * float(pitch)
#     return float(gravZ), n * 180 + math.pow(-1, n) * float(pitch), n
#
def correctYaw(prevyaw, yaw, n):
    if prevyaw >= 170 and prevyaw <=180 and float(yaw) >=-180 and float(yaw) <=-170:
        n += 1
    elif float(yaw) >= 170 and float(yaw) <=180 and prevyaw >=-180 and prevyaw <=-170:
        n -= 1

    prevyawnew = float(yaw)
    # print(nC, pitch, prevaccC, d3[az])
    yawnew = n * 360 + float(yaw)
    return prevyawnew, yawnew, n
#
def correctRoll(prevroll, roll, n):
    if prevroll >= 170 and prevroll <=180 and float(roll) >=-180 and float(roll) <=-170:
        n += 1
    elif float(roll) >= 170 and float(roll) <=180 and prevroll >=-180 and prevroll <=-170:
        n -= 1

    prevrollnew = float(roll)
    # print(nC, pitch, prevaccC, d3[az])
    rollnew = n * 360 + float(roll)
    return prevrollnew, rollnew, n

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



prevdata1 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata2 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata3 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata4 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata5 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata6 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata7 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

#  display_values => number of values to display at once on the plot
display_values = 500
x = np.linspace(0, display_values, display_values)

y1 = np.zeros(display_values)
y2 = np.zeros(display_values)
y3 = np.zeros(display_values)
y4 = np.zeros(display_values)
y5 = np.zeros(display_values)
y6 = np.zeros(display_values)
y7 = np.zeros(display_values)
y8 = np.zeros(display_values)
y9 = np.zeros(display_values)
y10 = np.zeros(display_values)

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-180, 180])
line1, = ax.plot(x, y1, 'b-', label='rollC')
line2, = ax.plot(x, y2, 'r-', label='rollD')
line3, = ax.plot(x, y3, 'y-', label='flexangleRight')
line4, = ax.plot(x, y4, 'g-', label='rollG')
line5, = ax.plot(x, y5, 'm-', label='rollN')
line6, = ax.plot(x, y6, 'k-', label='flexangleLeft')
# line7, = ax.plot(x, y7, 'c-', label='accZ-C')
# line8, = ax.plot(x, y8, 'tab:pink', label='nB')
# line9, = ax.plot(x, y9, 'tab:gray', label='accZ-B')
line10, = ax.plot(x, y10, 'tab:brown', label='hs')
ax.legend()
#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 50
counter = 0
k = 0
rate = 0

prevyawD = 0
prevyawC = 0
prevyawB = 0
prevyawN = 0
prevyawG = 0
nByaw = 0
nCyaw = 0
nDyaw = 0
nNyaw = 0
nGyaw = 0

prevrollD = 0
prevrollC = 0
prevrollB = 0
prevrollN = 0
prevrollG = 0
nBroll = 0
nCroll = 0
nDroll = 0
nNroll = 0
nGroll = 0

# name = input("Name of patient\n")
# joint = input("Name of joint\n")
name = "Box"
joint = "StaticOnBox"
trial = input("Trial number?\n")
file_name_all = '{}_{}_allSensorData_{}_{}_{}_{}.csv'.format(name, trial, datetime.now().date(), datetime.now().time().hour,
                                               datetime.now().time().minute, datetime.now().time().second)
file_name_diff_pitch = 'diff_pitch_{}_{}.csv'.format(name, trial)
file_name_gait_cycle = '{}_{}_gait_cycle.csv'.format(name, trial)
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(datetime.now().date()), '{}_{}_gait_cycle'.format(name, trial))
try:
    os.makedirs(dest_dir)
except OSError:
    pass  # already exists
path_all = os.path.join(dest_dir, file_name_all)
path_diff_pitch = os.path.join(dest_dir, file_name_diff_pitch)
path_gait_cycle = os.path.join(dest_dir, file_name_gait_cycle)

flagE = 0
flagD = 0
flagC = 0
flagB = 0
flagA = 0
flagG = 0
flagN = 0

countE = 0
countD = 0
countC = 0
countB = 0
countA = 0
countG = 0
countN = 0

initialtimeE = 0
initialtimeD = 0
initialtimeC = 0
initialtimeB = 0
initialtimeA = 0
initialtimeG = 0
initialtimeN = 0

rateE = 0
rateD = 0
rateC = 0
rateB = 0
rateA = 0
rateG = 0
rateN = 0

sendrateE = 0
sendrateD = 0
sendrateC = 0
sendrateB = 0
sendrateA = 0
sendrateG = 0
sendrateN = 0

sendinitialtimeE = 0
sendinitialtimeD = 0
sendinitialtimeC = 0
sendinitialtimeB = 0
sendinitialtimeA = 0
sendinitialtimeG = 0
sendinitialtimeN = 0

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0", 9999))
s1.setblocking(0)

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s2.bind(("0.0.0.0", 8888))
s2.setblocking(0)

s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s3.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s3.bind(("0.0.0.0", 7777))
s3.setblocking(0)

s4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s4.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s4.bind(("0.0.0.0", 6666))
s4.setblocking(0)

s5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s5.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s5.bind(("0.0.0.0", 5555))
s5.setblocking(0)

s6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s6.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s6.bind(("0.0.0.0", 4444))
s6.setblocking(0)

s7 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s7.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s7.bind(("0.0.0.0", 3333))
s7.setblocking(0)

with open(path_diff_pitch, 'w') as file1, open(path_all, 'w') as file2:
    file1.write('RightRoll1,RightRoll2,Rightflex_angle,RightPitch1,RightPitch2,Rightvar_angle,RightYaw1,RightYaw2,Rightrot_angle,LeftRoll1,LeftRoll2,Leftflex_angle,LeftPitch1,LeftPitch2,Leftvar_angle,LeftYaw1,LeftYaw2,Leftrot_angle,hs\n')
    file2.write(
        'FlagE,AccX_E,AccY_E,AccZ_E,GyroX_E,GyroY_E,GyroZ_E,_EQ1,_EQ2,_EQ3,_EQ4,_EYawQ,_EPitchQ,_ERollQ,_EYaw,_EPitch,_ERoll,_Ecount,_Etime,_EStep,_EDist,_ESendRate,_ERecvRate,FlagD,AccX_D,AccY_D,AccZ_D,GyroX_D,GyroY_D,GyroZ_D,_DQ1,_DQ2,_DQ3,_DQ4,_DYawQ,_DPitchQ,_DRollQ,_DYaw,_DPitch,_DRoll,_Dcount,_Dtime,_DHS,_DDist,_DgravaccX,_DgravaccY,_DgravaccZ,_DSendRate,_DRecvRate,FlagC,AccX_C,AccY_C,AccZ_C,GyroX_C,GyroY_C,GyroZ_C,_CQ1,_CQ2,_CQ3,_CQ4,_CYawQ,_CPitchQ,_CRollQ,_CYaw,_CPitch,_CRoll,_Ccount,_Ctime,_CHS,_CDist,_CgravaccX,_CgravaccY,_CgravaccZ,_CSendRate,_CRecvRate,FlagB,AccX_B,AccY_B,AccZ_B,GyroX_B,GyroY_B,GyroZ_B,_BQ1,_BQ2,_BQ3,_BQ4,_BYawQ,_BPitchQ,_BRollQ,_BYaw,_BPitch,_BRoll,_Bcount,_Btime,_BHS,_BDist,_BgravaccX,_BgravaccY,_BgravaccZ,_BSendRate,_BRecvRate,FlagA,AccX_A,AccY_A,AccZ_A,GyroX_A,GyroY_A,GyroZ_A,_AQ1,_AQ2,_AQ3,_AQ4,_AYawQ,_APitchQ,_ARollQ,_AYaw,_APitch,_ARoll,_Acount,_Atime,_AHS,_ADist,_AgravaccX,_AgravaccY,_AgravaccZ,_ASendRate,_ARecvRate,FlagG,AccX_G,AccY_G,AccZ_G,GyroX_G,GyroY_G,GyroZ_G,_GQ1,_GQ2,_GQ3,_GQ4,_GYawQ,_GPitchQ,_GRollQ,_GYaw,_GPitch,_GRoll,_Gcount,_Gtime,_GHS,_GDist,_GgravaccX,_GgravaccY,_GgravaccZ,_GSendRate,_GRecvRate,FlagN,AccX_N,AccY_N,AccZ_N,GyroX_N,GyroY_N,GyroZ_N,_NQ1,_NQ2,_NQ3,_NQ4,_NYawQ,_NPitchQ,_NRollQ,_NYaw,_NPitch,_NRoll,_Ncount,_Ntime,_NHS,_NDist,_NgravaccX,_NgravaccY,_NgravaccZ,_NSendRate,_NRecvRate,rate,time' + '\n')
    while not keyboard.is_pressed("q"):
        if counter == 0:
            cur_time = time.time()
        counter+=1
        if time.time() - cur_time > 1:
            rate = counter/ (time.time() - cur_time)
            counter=0

        try:
            data1 = s1.recv(1024).decode("utf-8")
            prevdata1 = data1
            flagE = 1
            if countE == 0:
                initialtimeE = time.time()
                # sendinitialtimeE = str(data1).split(',')[timer]
            countE += 1
            if time.time() - initialtimeE > 1:
                rateE = countE / (time.time() - initialtimeE)
                # sendrateE = countE / (str(data1).split(',')[timer] - sendinitialtimeE)
                countE = 0
        except socket.error:
            data1 = prevdata1
            flagE = 0

        d1 = str(data1).split(',')

        try:
            data2 = s2.recv(1024).decode("utf-8")
            prevdata2 = data2
            flagD = 1
            if countD == 0:
                initialtimeD = time.time()
                sendinitialtimeD = str(data2).split(',')[timer]
            countD += 1
            if time.time() - initialtimeD > 1:
                rateD = countD / (time.time() - initialtimeD)
                sendrateD = countD / (str(data2).split(',')[timer] - sendinitialtimeD)
                countD = 0
        except socket.error:
            data2 = prevdata2
            flagD = 0

        d2 = str(data2).split(',')

        try:
            data3 = s3.recv(1024).decode("utf-8")
            prevdata3 = data3
            flagC = 1
            if countC == 0:
                initialtimeC = time.time()
                sendinitialtimeC = str(data3).split(',')[timer]
            countC += 1
            if time.time() - initialtimeC > 1:
                rateC = countC / (time.time() - initialtimeC)
                sendrateC = countC / (str(data3).split(',')[timer] - sendinitialtimeC)
                countC = 0
        except socket.error:
            data3 = prevdata3
            flagC = 0

        d3 = str(data3).split(',')

        try:
            data4 = s4.recv(1024).decode("utf-8")
            prevdata4 = data4
            flagB = 1
            if countB == 0:
                initialtimeB = time.time()
                sendinitialtimeB = str(data4).split(',')[timer]
            countB += 1
            if time.time() - initialtimeB > 1:
                rateB = countB / (time.time() - initialtimeB)
                sendrateB = countB / (str(data4).split(',')[timer] - sendinitialtimeB)
                countB = 0
        except socket.error:
            data4 = prevdata4
            flagB = 0

        d4 = str(data4).split(',')

        try:
            data5 = s5.recv(1024).decode("utf-8")
            prevdata5 = data5
            flagA = 1
            if countA == 0:
                initialtimeA = time.time()
                sendinitialtimeA = str(data5).split(',')[timer]
            countA += 1
            if time.time() - initialtimeA > 1:
                rateA = countA / (time.time() - initialtimeA)
                sendrateA = countA / (str(data5).split(',')[timer] - sendinitialtimeA)
                countA = 0
        except socket.error:
            data5 = prevdata5
            flagA = 0

        d5 = str(data5).split(',')

        try:
            data6 = s6.recv(1024).decode("utf-8")
            prevdata6 = data6
            flagG = 1
            if countG == 0:
                initialtimeG = time.time()
                sendinitialtimeG = str(data6).split(',')[timer]
            countG += 1
            if time.time() - initialtimeG > 1:
                rateG = countG / (time.time() - initialtimeG)
                sendrateG = countG / (str(data6).split(',')[timer] - sendinitialtimeG)
                countG = 0
        except socket.error:
            data6 = prevdata6
            flagG = 0

        d6 = str(data6).split(',')

        try:
            data7 = s7.recv(1024).decode("utf-8")
            prevdata7 = data7
            flagN = 1
            if countN == 0:
                initialtimeN = time.time()
                sendinitialtimeN = str(data7).split(',')[timer]
            countN += 1
            if time.time() - initialtimeN > 1:
                rateN = countN / (time.time() - initialtimeN)
                sendrateN = countE / (str(data7).split(',')[timer] - sendinitialtimeN)
                countN = 0
        except socket.error:
            data7 = prevdata7
            flagN = 0

        d7 = str(data7).split(',')

        prevyawD, d2[calcYaw], nDyaw = correctYaw(prevyawD, d2[calcYaw], nDyaw)
        prevyawC, d3[calcYaw], nCyaw = correctYaw(prevyawC, d3[calcYaw], nCyaw)
        prevyawB, d4[calcYaw], nByaw = correctYaw(prevyawB, d4[calcYaw], nByaw)
        prevyawG, d6[calcYaw], nGyaw = correctYaw(prevyawG, d6[calcYaw], nGyaw)
        prevyawN, d7[calcYaw], nNyaw = correctYaw(prevyawN, d7[calcYaw], nNyaw)

        prevrollD, d2[calcRoll], nDroll = correctRoll(prevrollD, d2[calcRoll], nDroll)
        prevrollC, d3[calcRoll], nCroll = correctRoll(prevrollC, d3[calcRoll], nCroll)
        prevrollB, d4[calcRoll], nBroll = correctRoll(prevrollB, d4[calcRoll], nBroll)
        prevrollG, d6[calcRoll], nGroll = correctRoll(prevrollG, d6[calcRoll], nGroll)
        prevrollN, d7[calcRoll], nNroll = correctRoll(prevrollN, d7[calcRoll], nNroll)

        y1 = np.roll(y1, -1)
        y1[-1] = d3[calcRoll]

        y2 = np.roll(y2, -1)
        y2[-1] = d2[calcRoll]

        y3 = np.roll(y3, -1)
        y3[-1] = y2[-1] - y1[-1]

        y4 = np.roll(y4, -1)
        y4[-1] = d3[calcPitch]

        y5 = np.roll(y5, -1)
        y5[-1] = d2[calcPitch]

        y6 = np.roll(y6, -1)
        y6[-1] = y5[-1] - y4[-1]

        y7 = np.roll(y7, -1)
        y7[-1] = d3[calcYaw]

        y8 = np.roll(y8, -1)
        y8[-1] = d2[calcYaw]

        y9 = np.roll(y9, -1)
        y9[-1] = y8[-1] - y7[-1]

        y11 = np.roll(y11, -1)
        y11[-1] = d4[calcRoll]

        y12 = np.roll(y12, -1)
        y12[-1] = d7[calcRoll]

        y13 = np.roll(y13, -1)
        y13[-1] = y12[-1] - y11[-1]

        y14 = np.roll(y14, -1)
        y14[-1] = d4[calcPitch]

        y15 = np.roll(y15, -1)
        y15[-1] = d7[calcPitch]

        y16 = np.roll(y16, -1)
        y16[-1] = y15[-1] - y14[-1]

        y17 = np.roll(y17, -1)
        y17[-1] = d4[calcYaw]

        y18 = np.roll(y18, -1)
        y18[-1] = d7[calcYaw]

        y19 = np.roll(y19, -1)
        y19[-1] = y18[-1] - y17[-1]

        y10 = np.roll(y10, -1)
        y10[-1] = int(d1[hs]) * 100

        file1.write(str(y1[-1]) + ',' + str(y2[-1]) + ',' + str(y3[-1]) + ',' + str(y4[-1]) + ',' + str(y5[-1]) + ',' + str(y6[-1]) + ',' + str(y7[-1]) + ',' + str(y8[-1]) + ',' + str(y9[-1]) + ',' +
                    str(y11[-1]) + ',' + str(y12[-1]) + ',' + str(y13[-1]) + ',' + str(y14[-1]) + ',' + str(y15[-1]) + ',' + str(y16[-1]) + ',' + str(y17[-1]) + ',' + str(y18[-1]) + ',' + str(y19[-1]) + ',' +
                    str(y10[-1]) + '\n')
        file2.write(str(flagE) + ',' +str(data1) + ',' + str(sendrateE) + ',' +str(rateE) + ',' +
                    str(flagD) + ',' +str(data2) + ',' + str(sendrateD) + ',' +str(rateD) + ',' +
                    str(flagC) + ',' +str(data3) + ',' + str(sendrateC) + ',' +str(rateC) + ',' +
                    str(flagB) + ',' +str(data4) + ',' + str(sendrateB) + ',' +str(rateB) + ',' +
                    str(flagA) + ',' +str(data5) + ',' + str(sendrateA) + ',' +str(rateA) + ',' +
                    str(flagG) + ',' +str(data6) + ',' + str(sendrateG) + ',' +str(rateG) + ',' +
                    str(flagN) + ',' +str(data7) + ',' + str(sendrateN) + ',' +str(rateN) + ',' +
                    str(rate) + ',' + str(time.time()) + '\n')
        k = k + 1
        # count += 1
        # print("Data rate=",rate)
        if k == r:
            line1.set_ydata(y1)
            line2.set_ydata(y2)
            line3.set_ydata(y3)
            line4.set_ydata(y11)
            line5.set_ydata(y12)
            line6.set_ydata(y13)
            # line7.set_ydata(y7)
            # line8.set_ydata(y8)
            # line9.set_ydata(y9)
            line10.set_ydata(y10)
            fig.canvas.draw()
            fig.canvas.flush_events()
            k = 0

dest_path = gait.add_gait_cycle(path_gait_cycle, path_diff_pitch, joint)