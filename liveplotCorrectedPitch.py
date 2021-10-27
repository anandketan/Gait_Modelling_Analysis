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
line1, = ax.plot(x, y1, 'b-', label='pitchC')
line2, = ax.plot(x, y2, 'r-', label='pitchB')
line3, = ax.plot(x, y3, 'y-', label='diffpitch')
# line4, = ax.plot(x, y4, 'g-', label='pitchCdirect')
# line5, = ax.plot(x, y5, 'm-', label='pitchBdirect')
# line6, = ax.plot(x, y6, 'k-', label='nC')
# line7, = ax.plot(x, y7, 'c-', label='accZ-C')
# line8, = ax.plot(x, y8, 'tab:pink', label='nB')
# line9, = ax.plot(x, y9, 'tab:gray', label='accZ-B')
line10, = ax.plot(x, y10, 'tab:brown', label='hs')
ax.legend()
#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 50
count = 0
k = 0
rate = 0

prevaccC = 0
prevaccB = 0
# prevpitchB = 0
nB = 0
nC = 0
# firstC = 0
# firstB = 0
# limit = 80

name = input("Name of patient\n")
joint = input("Name of joint\n")
trial = input("Trial number?\n")
file_name_all = '{}_{}_{}_{}_{}_{}.csv'.format(name, trial, datetime.now().date(), datetime.now().time().hour,
                                               datetime.now().time().minute, datetime.now().time().second)
file_name_diff_pitch = 'diff_pitch_{}_{}.csv'.format(name, trial)
file_name_gait_cycle = '{}_{}_gait_cycle.csv'.format(name, trial)
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint))
try:
    os.makedirs(dest_dir)
except OSError:
    pass  # already exists
path_all = os.path.join(dest_dir, file_name_all)
path_diff_pitch = os.path.join(dest_dir, file_name_diff_pitch)
path_gait_cycle = os.path.join(dest_dir, file_name_gait_cycle)

with open(path_diff_pitch, 'w') as file1, open(path_all, 'w') as file2:
    file1.write('Pitch1,Pitch2,diff_pitch,hs\n')
    file2.write(
        'AccX_E,AccY_E,AccZ_E,GyroX_E,GyroY_E,GyroZ_E,_EQ1,_EQ2,_EQ3,_EQ4,_EYawQ,_EPitchQ,_ERollQ,_EYaw,_EPitch,_ERoll,_Ecount,_Etime,_EStep,_EDist,AccX_D,AccY_D,AccZ_D,GyroX_D,GyroY_D,GyroZ_D,_DQ1,_DQ2,_DQ3,_DQ4,_DYawQ,_DPitchQ,_DRollQ,_DYaw,_DPitch,_DRoll,_Dcount,_Dtime,_DHS,_DDist,_DgravaccX,_DgravaccY,_DgravaccZ,AccX_C,AccY_C,AccZ_C,GyroX_C,GyroY_C,GyroZ_C,_CQ1,_CQ2,_CQ3,_CQ4,_CYawQ,_CPitchQ,_CRollQ,_CYaw,_CPitch,_CRoll,_Ccount,_Ctime,_CHS,_CDist,_CgravaccX,_CgravaccY,_CgravaccZ,AccX_B,AccY_B,AccZ_B,GyroX_B,GyroY_B,GyroZ_B,_BQ1,_BQ2,_BQ3,_BQ4,_BYawQ,_BPitchQ,_BRollQ,_BYaw,_BPitch,_BRoll,_Bcount,_Btime,_BHS,_BDist,_BgravaccX,_BgravaccY,_BgravaccZ,AccX_A,AccY_A,AccZ_A,GyroX_A,GyroY_A,GyroZ_A,_AQ1,_AQ2,_AQ3,_AQ4,_AYawQ,_APitchQ,_ARollQ,_AYaw,_APitch,_ARoll,_Acount,_Atime,_AHS,_ADist,_AgravaccX,_AgravaccY,_AgravaccZ,AccX_G,AccY_G,AccZ_G,GyroX_G,GyroY_G,GyroZ_G,_GQ1,_GQ2,_GQ3,_GQ4,_GYawQ,_GPitchQ,_GRollQ,_GYaw,_GPitch,_GRoll,_Gcount,_Gtime,_GHS,_GDist,_GgravaccX,_GgravaccY,_GgravaccZ,AccX_N,AccY_N,AccZ_N,GyroX_N,GyroY_N,GyroZ_N,_NQ1,_NQ2,_NQ3,_NQ4,_NYawQ,_NPitchQ,_NRollQ,_NYaw,_NPitch,_NRoll,_Ncount,_Ntime,_NHS,_NDist,_NgravaccX,_NgravaccY,_NgravaccZ,rate,time' + '\n')
    while not keyboard.is_pressed("q"):
        if (count % 100) == 0:
            cur_time = time.time()
        if (count % 100) == 99:
            rate = 99 / (time.time() - cur_time)

        try:
            data1 = s1.recv(1024).decode("utf-8")
            prevdata1 = data1
        except socket.error:
            data1 = prevdata1

        d1 = str(data1).split(',')

        try:
            data2 = s2.recv(1024).decode("utf-8")
            prevdata2 = data2
        except socket.error:
            data2 = prevdata2

        d2 = str(data2).split(',')

        try:
            data3 = s3.recv(1024).decode("utf-8")
            prevdata3 = data3
        except socket.error:
            data3 = prevdata3

        d3 = str(data3).split(',')

        try:
            data4 = s4.recv(1024).decode("utf-8")
            prevdata4 = data4
        except socket.error:
            data4 = prevdata4

        d4 = str(data4).split(',')

        try:
            data5 = s5.recv(1024).decode("utf-8")
            prevdata5 = data5
        except socket.error:
            data5 = prevdata5

        d5 = str(data5).split(',')

        try:
            data6 = s6.recv(1024).decode("utf-8")
            prevdata6 = data6
        except socket.error:
            data6 = prevdata6

        d6 = str(data6).split(',')

        try:
            data7 = s7.recv(1024).decode("utf-8")
            prevdata7 = data7
        except socket.error:
            data7 = prevdata7

        d7 = str(data7).split(',')

        # y4 = np.roll(y4, -1)
        # y4[-1] = d3[Pitch]

        # y5 = np.roll(y5, -1)
        # y5[-1] = d4[Pitch]

        if prevaccC > 0 and float(d3[gravaccz]) <= 0 and float(d3[Pitch]) > 0:
            nC -= 1
        elif prevaccC > 0 and float(d3[gravaccz]) <= 0 and float(d3[Pitch]) < 0:
            nC += 1
        elif prevaccC <= 0 and float(d3[gravaccz]) > 0 and float(d3[Pitch]) > 0:
            nC += 1
        elif prevaccC <= 0 and float(d3[gravaccz]) > 0 and float(d3[Pitch]) < 0:
            nC -= 1

        prevaccC = float(d3[gravaccz])
        print(nC, d3[Pitch], prevaccC, d3[az])
        d3[Pitch] = nC * 180 + math.pow(-1, nC) * float(d3[Pitch])

        if prevaccB > 0 and float(d4[gravaccz]) <= 0 and float(d4[Pitch]) > 0:
            nB -= 1
        elif prevaccB > 0 and float(d4[gravaccz]) <= 0 and float(d4[Pitch]) < 0:
            nB += 1
        elif prevaccB <= 0 and float(d4[gravaccz]) > 0 and float(d4[Pitch]) > 0:
            nB += 1
        elif prevaccB <= 0 and float(d4[gravaccz]) > 0 and float(d4[Pitch]) < 0:
            nB -= 1

        prevaccB = float(d4[gravaccz])
        print(nB, d4[Pitch], prevaccB, d4[az])
        d4[Pitch] = nB * 180 + math.pow(-1, nB) * float(d4[Pitch])

        y1 = np.roll(y1, -1)
        y1[-1] = d3[Pitch]

        y2 = np.roll(y2, -1)
        y2[-1] = d4[Pitch]

        y3 = np.roll(y3, -1)
        y3[-1] = abs(y2[-1] - y1[-1])

        # y6 = np.roll(y6, -1)
        # y6[-1] = int(nC)*10

        # y7 = np.roll(y7, -1)
        # y7[-1] = float(d3[gravaccz])*10

        # y8 = np.roll(y8, -1)
        # y8[-1] = int(nB)*10

        # y9 = np.roll(y9, -1)
        # y9[-1] = float(d4[gravaccz])*10

        y10 = np.roll(y10, -1)
        y10[-1] = int(d1[hs]) * 100

        file1.write(str(y1[-1]) + ',' + str(y2[-1]) + ',' + str(y3[-1]) + ',' + str(y10[-1]) + '\n')
        file2.write(str(data1) + ',' + str(data2) + ',' + str(data3) + ',' + str(data4) + ',' + str(data5) + ',' + str(
            data6) + ',' + str(data7) + ',' + str(rate) + ',' + str(time.time()) + '\n')
        # file2.write(str(y4[-1])+','+str(y1[-1])+','+str(prevaccC)+','+str(y7[-1])+','+str(nC)+'\n')
        # print(k)
        k = k + 1
        count += 1
        # print("Data rate=",rate)
        if k == r:
            line1.set_ydata(y1)
            line2.set_ydata(y2)
            line3.set_ydata(y3)
            # line4.set_ydata(y4)
            # line5.set_ydata(y5)
            # line6.set_ydata(y6)
            # line7.set_ydata(y7)
            # line8.set_ydata(y8)
            # line9.set_ydata(y9)
            line10.set_ydata(y10)
            fig.canvas.draw()
            fig.canvas.flush_events()
            k = 0

dest_path = gait.add_gait_cycle(path_gait_cycle, path_diff_pitch, joint)