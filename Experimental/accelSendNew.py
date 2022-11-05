import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import math
import os
import datetime
from datetime import datetime

def correctYaw(prevyaw, yaw, n):
    if prevyaw >= 160 and prevyaw <=180 and float(yaw) >=-180 and float(yaw) <=-160:
        n += 1
    elif float(yaw) >= 160 and float(yaw) <=180 and prevyaw >=-180 and prevyaw <=-160:
        n -= 1

    prevyawnew = float(yaw)
    # print(nC, pitch, prevaccC, d3[az])
    yawnew = n * 360 + float(yaw)
    return prevyawnew, yawnew, n
#
def correctRoll(prevroll, roll, n):
    if prevroll >= 160 and prevroll <=180 and float(roll) >=-180 and float(roll) <=-160:
        n += 1
    elif float(roll) >= 160 and float(roll) <=180 and prevroll >=-180 and prevroll <=-160:
        n -= 1

    prevrollnew = float(roll)
    # print(nC, pitch, prevaccC, d3[az])
    rollnew = n * 360 + float(roll)
    return prevrollnew, rollnew, n

def correctPitch(prevpitch, pitch, n):
    prevpitchnew = float(pitch)
    pitchnew = float(pitch)
    return prevpitchnew, pitchnew, n

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

prevpitchD = 0
prevpitchC = 0
prevpitchB = 0
prevpitchN = 0
prevpitchG = 0
nBpitch = 0
nCpitch = 0
nDpitch = 0
nNpitch = 0
nGpitch = 0

name = 'Ritish'
trial = '2'
file_name_all = '{}_{}_allGameSensorData_{}_{}_{}_{}.csv'.format(name, trial, datetime.now().date(), datetime.now().time().hour,
                                               datetime.now().time().minute, datetime.now().time().second)
file_name_pose = 'diff_pitch_{}_{}.csv'.format(name, trial)
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}'.format(datetime.now().date()), '{}_{}'.format(name, trial))
try:
    os.makedirs(dest_dir)
except OSError:
    pass # already exists
path_game = os.path.join(dest_dir, file_name_all)
path_pose = os.path.join(dest_dir, file_name_pose)

#UDP_IP = "192.168.100.1"
UDP_IP = "127.0.0.1"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

pose_detect = ""
step = 0
reach = 0
forward = 0
side = 0

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

sumE = 0.0
sumD = 0.0
sumC = 0.0
sumB = 0.0
sumA = 0.0
sumG = 0.0
sumN = 0.0

initial_calE = 0
initial_calD = 0
initial_calC = 0
initial_calB = 0
initial_calA = 0
initial_calG = 0
initial_calN = 0

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
s3.bind(("0.0.0.0", 3333))
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
s7.bind(("0.0.0.0", 7777))
s7.setblocking(0)



with open(path_pose, 'w') as file1, open(path_game, 'w') as file2:
    file1.write(
        'RAUGravAccX,RAUGravAccY,RAUGravAccZ,RALGravAccX,RALGravAccY,RALGravAccZ,RA_diff_roll,RA_diff_pitch,RA_diff_yaw,Reach,'
        'RLUGravAccX,RLUGravAccY,RLUGravAccZ,RLLGravAccX,RLLGravAccY,RLLGravAccZ,RL_diff_roll,RL_diff_pitch,RL_diff_yaw,Step,'
        'BackGravAccX,BackGravAccY,BackGravAccZ,Back_roll,Back_pitch,Back_yaw,Forward,Sway'
        '\n')
    file2.write(
        'FlagE,AccX_E,AccY_E,AccZ_E,GyroX_E,GyroY_E,GyroZ_E,_EQ1,_EQ2,_EQ3,_EQ4,_EYawQ,_EPitchQ,_ERollQ,_EYaw,_EPitch,_ERoll,_Ecount,_Etime,_EStep,_EDist,_ESendRate,_ERecvRate,'
        'FlagD,AccX_D,AccY_D,AccZ_D,GyroX_D,GyroY_D,GyroZ_D,_DQ1,_DQ2,_DQ3,_DQ4,_DYawQ,_DPitchQ,_DRollQ,_DYaw,_DPitch,_DRoll,_Dcount,_Dtime,_DHS,_DDist,_DgravaccX,_DgravaccY,_DgravaccZ,_DSendRate,_DRecvRate,'
        'FlagC,AccX_C,AccY_C,AccZ_C,GyroX_C,GyroY_C,GyroZ_C,_CQ1,_CQ2,_CQ3,_CQ4,_CYawQ,_CPitchQ,_CRollQ,_CYaw,_CPitch,_CRoll,_Ccount,_Ctime,_CHS,_CDist,_CgravaccX,_CgravaccY,_CgravaccZ,_CSendRate,_CRecvRate,'
        'FlagB,AccX_B,AccY_B,AccZ_B,GyroX_B,GyroY_B,GyroZ_B,_BQ1,_BQ2,_BQ3,_BQ4,_BYawQ,_BPitchQ,_BRollQ,_BYaw,_BPitch,_BRoll,_Bcount,_Btime,_BHS,_BDist,_BgravaccX,_BgravaccY,_BgravaccZ,_BSendRate,_BRecvRate,'
        'FlagA,AccX_A,AccY_A,AccZ_A,GyroX_A,GyroY_A,GyroZ_A,_AQ1,_AQ2,_AQ3,_AQ4,_AYawQ,_APitchQ,_ARollQ,_AYaw,_APitch,_ARoll,_Acount,_Atime,_AHS,_ADist,_AgravaccX,_AgravaccY,_AgravaccZ,_ASendRate,_ARecvRate,'
        'FlagG,AccX_G,AccY_G,AccZ_G,GyroX_G,GyroY_G,GyroZ_G,_GQ1,_GQ2,_GQ3,_GQ4,_GYawQ,_GPitchQ,_GRollQ,_GYaw,_GPitch,_GRoll,_Gcount,_Gtime,_GHS,_GDist,_GgravaccX,_GgravaccY,_GgravaccZ,_GSendRate,_GRecvRate,'
        'FlagN,AccX_N,AccY_N,AccZ_N,GyroX_N,GyroY_N,GyroZ_N,_NQ1,_NQ2,_NQ3,_NQ4,_NYawQ,_NPitchQ,_NRollQ,_NYaw,_NPitch,_NRoll,_Ncount,_Ntime,_NHS,_NDist,_NgravaccX,_NgravaccY,_NgravaccZ,_NSendRate,_NRecvRate,rate,time' + '\n')
    while True:
        if counter == 0:
            cur_time = time.time()
        counter += 1
        if time.time() - cur_time > 1:
            rate = counter / (time.time() - cur_time)
            counter = 0

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
                sendinitialtimeD = int(str(data2).split(',')[timer])
            countD += 1
            if time.time() - initialtimeD > 1:
                rateD = countD / (time.time() - initialtimeD)
                sendrateD = 1000 * countD / (int(str(data2).split(',')[timer]) - sendinitialtimeD)
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
                sendinitialtimeC = int(str(data3).split(',')[timer])
            countC += 1
            if time.time() - initialtimeC > 1:
                rateC = countC / (time.time() - initialtimeC)
                sendrateC = 1000 * countC / (int(str(data3).split(',')[timer]) - sendinitialtimeC)
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
                sendinitialtimeB = int(str(data4).split(',')[timer])
                print(initialtimeB, sendinitialtimeB)
            countB += 1
            if time.time() - initialtimeB > 1:
                print(countB,time.time(),initialtimeB,int(str(data4).split(',')[timer]),sendinitialtimeB)
                rateB = countB / (time.time() - initialtimeB)
                sendrateB = 1000 * countB / (int(str(data4).split(',')[timer]) - sendinitialtimeB)
                print(rateB, sendrateB)
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
                sendinitialtimeA = int(str(data5).split(',')[timer])
            countA += 1
            if time.time() - initialtimeA > 1:
                rateA = countA / (time.time() - initialtimeA)
                sendrateA = 1000 * countA / (int(str(data5).split(',')[timer]) - sendinitialtimeA)
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
                sendinitialtimeG = int(str(data6).split(',')[timer])
            countG += 1
            if time.time() - initialtimeG > 1:
                rateG = countG / (time.time() - initialtimeG)
                sendrateG = 1000 * countG / (int(str(data6).split(',')[timer]) - sendinitialtimeG)
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
                sendinitialtimeN = int(str(data7).split(',')[timer])
            countN += 1
            if time.time() - initialtimeN > 1:
                rateN = countN / (time.time() - initialtimeN)
                sendrateN = 1000 * countN / (int(str(data7).split(',')[timer]) - sendinitialtimeN)
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

        prevpitchD, d2[calcPitch], nDpitch = correctPitch(prevpitchD, d2[calcPitch], nDpitch)
        prevpitchC, d3[calcPitch], nCpitch = correctPitch(prevpitchC, d3[calcPitch], nCpitch)
        prevpitchB, d4[calcPitch], nBpitch = correctPitch(prevpitchB, d4[calcPitch], nBpitch)
        prevpitchG, d6[calcPitch], nGpitch = correctPitch(prevpitchG, d6[calcPitch], nGpitch)
        prevpitchN, d7[calcPitch], nNpitch = correctPitch(prevpitchN, d7[calcPitch], nNpitch)

        pose_detect = str(d6[gravaccx]) + "," + str(d6[gravaccy]) + "," + str(d6[gravaccz]) + "," +\
                      str(d2[gravaccx]) + "," + str(d2[gravaccy]) + "," + str(d2[gravaccz]) + "," +\
                      str(d7[gravaccx]) + "," + str(d7[gravaccy]) + "," + str(d7[gravaccz]) + "," +\
                      str(d3[gravaccx]) + "," + str(d3[gravaccy]) + "," + str(d3[gravaccz]) + "," +\
                      str(d4[gravaccx]) + "," + str(d4[gravaccy]) + "," + str(d4[gravaccz])
        #print("Acceleration - ", pose_detect)
        print(d4[gravaccx], d4[gravaccy], d4[gravaccz])
        print("----------------------")
        print(d3[gravaccx], d3[gravaccy], d3[gravaccz])
        print("=============")
        print(d2[gravaccx])
        sock.sendto(pose_detect.encode(),(UDP_IP, UDP_PORT))

        # if countG > 500:
        #     pose_detect = str(d6[gravaccx]) + "," + str(d6[gravaccy]) + "," + str(d6[gravaccz]) + "," +\
        #                   str(d2[gravaccx]) + "," + str(d2[gravaccy]) + "," + str(d2[gravaccz]) + "," +\
        #                   str(d7[gravaccx]) + "," + str(d7[gravaccy]) + "," + str(d7[gravaccz]) + "," +\
        #                   str(d3[gravaccx]) + "," + str(d3[gravaccy]) + "," + str(d3[gravaccz]) + "," +\
        #                   str(d4[gravaccx]) + "," + str(d4[gravaccy]) + "," + str(d4[gravaccz])
        #     print("Acceleration - ", pose_detect)
        #     sock.sendto(pose_detect.encode(),(UDP_IP, UDP_PORT))
        #elif countG <=500:
            #print("Stand still for calibration")

        # print(countG, countN, countB, countC, countD)
        raRoll = d2[calcRoll] - d7[calcRoll]
        raYaw = d2[calcYaw] - d7[calcYaw]
        raPitch = d2[calcPitch] - d7[calcPitch]
        rlRoll = d3[calcRoll] - d4[calcRoll]
        rlYaw = d3[calcYaw] - d4[calcYaw]
        rlPitch = d3[calcPitch] - d4[calcPitch]

        if float(d2[gravaccx]) > 2.5 and float(d7[gravaccx]) > 2.5 and float(d2[gravaccy]) < 0:
            reach = 1
        else:
            reach = 0

        if ((float(d3[gravaccz]) < 0 and float(d4[gravaccz]) < 0) or float(d3[gravaccz]) < -2 or float(d4[gravaccz]) < -2) and (float(d3[gravaccy]) > -2.5 and float(d3[gravaccy]) < 2.5) and (float(d4[gravaccy]) > -2.5 and float(d4[gravaccy]) < 2.5) and float(d3[gravaccx]) < 0 and float(d3[gravaccx]) < 0:
            step = 1
            #print("Step")
        else:
            step = 0
            #print("No Step")

        file1.write(
            str(d2[gravaccx]) + ',' + str(d2[gravaccy]) + ',' + str(d2[gravaccz]) + ',' + str(d7[gravaccx]) + ',' + str(d7[gravaccy]) + ',' + str(d7[gravaccz]) + ',' + str(raRoll) + ',' + str(raPitch) + ',' + str(raYaw) + ',' + str(reach) + ',' +
            str(d3[gravaccx]) + ',' + str(d3[gravaccy]) + ',' + str(d3[gravaccz]) + ',' + str(d4[gravaccx]) + ',' + str(d4[gravaccy]) + ',' + str(d4[gravaccz]) + ',' + str(rlRoll) + ',' + str(rlPitch) + ',' + str(rlYaw) + ',' + str(step) + ',' +
            str(d6[gravaccx]) + ',' + str(d6[gravaccy]) + ',' + str(d6[gravaccz]) + ',' + str(d6[calcRoll]) + ',' + str(d6[calcPitch]) + ',' + str(d6[calcYaw]) + ',' + str(forward) + ',' + str(side) + ','
            + '\n')
        file2.write(str(flagE) + ',' + str(data1) + ',' + str(sendrateE) + ',' + str(rateE) + ',' +
                    str(flagD) + ',' + str(data2) + ',' + str(sendrateD) + ',' + str(rateD) + ',' +
                    str(flagC) + ',' + str(data3) + ',' + str(sendrateC) + ',' + str(rateC) + ',' +
                    str(flagB) + ',' + str(data4) + ',' + str(sendrateB) + ',' + str(rateB) + ',' +
                    str(flagA) + ',' + str(data5) + ',' + str(sendrateA) + ',' + str(rateA) + ',' +
                    str(flagG) + ',' + str(data6) + ',' + str(sendrateG) + ',' + str(rateG) + ',' +
                    str(flagN) + ',' + str(data7) + ',' + str(sendrateN) + ',' + str(rateN) + ',' +
                    str(rate) + ',' + str(time.time()) + '\n')
