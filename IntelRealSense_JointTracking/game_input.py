import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import math
import os
import datetime
from datetime import datetime

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


s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0",9999))
s1.setblocking(0)

s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s2.bind(("0.0.0.0",8888))
s2.setblocking(0)

s3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s3.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s3.bind(("0.0.0.0",7777))
s3.setblocking(0)

s4 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s4.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s4.bind(("0.0.0.0",6666))
s4.setblocking(0)

s5 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s5.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s5.bind(("0.0.0.0",5555))
s5.setblocking(0)

s6 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s6.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s6.bind(("0.0.0.0",4444))
s6.setblocking(0)

s7 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s7.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s7.bind(("0.0.0.0",3333))
s7.setblocking(0)


prevdata1 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata2 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata3 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata4 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata5 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata6 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata7 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"


count=0
k = 0
rate = 0

prevaccD = 0
prevaccN = 0
prevaccG = 0
nD = 0
nN = 0
nG = 0

file_name_game = 'game_data.csv'
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}_{}_{}_{}'.format(datetime.now().date(), datetime.now().time().hour, datetime.now().time().minute, datetime.now().time().second))
try:
    os.makedirs(dest_dir)
except OSError:
    pass # already exists
path_game = os.path.join(dest_dir, file_name_game)

UDP_IP ="192.168.0.1"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

pose_detect = ""
reach_out1 = ""
reach_out2 = ""
reach_out = ""
step_out = ""
forward = ""

countE = 0
countD = 0
countC = 0
countB = 0
countA = 0
countG = 0
countN = 0

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

with open(path_game,'w') as file:
    file.write('AccX_E,AccY_E,AccZ_E,GyroX_E,GyroY_E,GyroZ_E,_EQ1,_EQ2,_EQ3,_EQ4,_EYawQ,_EPitchQ,_ERollQ,_EYaw,_EPitch,_ERoll,_Ecount,_Etime,_EStep,_EDist,AccX_D,AccY_D,AccZ_D,GyroX_D,GyroY_D,GyroZ_D,_DQ1,_DQ2,_DQ3,_DQ4,_DYawQ,_DPitchQ,_DRollQ,_DYaw,_DPitch,_DRoll,_Dcount,_Dtime,_DHS,_DDist,_DgravaccX,_DgravaccY,_DgravaccZ,AccX_C,AccY_C,AccZ_C,GyroX_C,GyroY_C,GyroZ_C,_CQ1,_CQ2,_CQ3,_CQ4,_CYawQ,_CPitchQ,_CRollQ,_CYaw,_CPitch,_CRoll,_Ccount,_Ctime,_CHS,_CDist,_CgravaccX,_CgravaccY,_CgravaccZ,AccX_B,AccY_B,AccZ_B,GyroX_B,GyroY_B,GyroZ_B,_BQ1,_BQ2,_BQ3,_BQ4,_BYawQ,_BPitchQ,_BRollQ,_BYaw,_BPitch,_BRoll,_Bcount,_Btime,_BHS,_BDist,_BgravaccX,_BgravaccY,_BgravaccZ,AccX_A,AccY_A,AccZ_A,GyroX_A,GyroY_A,GyroZ_A,_AQ1,_AQ2,_AQ3,_AQ4,_AYawQ,_APitchQ,_ARollQ,_AYaw,_APitch,_ARoll,_Acount,_Atime,_AHS,_ADist,_AgravaccX,_AgravaccY,_AgravaccZ,AccX_G,AccY_G,AccZ_G,GyroX_G,GyroY_G,GyroZ_G,_GQ1,_GQ2,_GQ3,_GQ4,_GYawQ,_GPitchQ,_GRollQ,_GYaw,_GPitch,_GRoll,_Gcount,_Gtime,_GHS,_GDist,_GgravaccX,_GgravaccY,_GgravaccZ,AccX_N,AccY_N,AccZ_N,GyroX_N,GyroY_N,GyroZ_N,_NQ1,_NQ2,_NQ3,_NQ4,_NYawQ,_NPitchQ,_NRollQ,_NYaw,_NPitch,_NRoll,_Ncount,_Ntime,_NHS,_NDist,_NgravaccX,_NgravaccY,_NgravaccZ,rate,time'+'\n')
    # file2.write('PitchC,calcPitchC,PrevAccC,CurAccC,nC\n')
    while True:
        if (count%100)==0:
            cur_time=time.time()
        if (count%100)==99:
            try:
                rate=99/(time.time()-cur_time)
            except:
                rate = 0

        try:
            data1 = s1.recv(1024).decode("utf-8")
            prevdata1 = data1
            countE+=1
        except socket.error:
            data1 = prevdata1
        
        d1 = str(data1).split(',')

        try:
            data2 = s2.recv(1024).decode("utf-8")
            prevdata2 = data2
            countD+=1
        except socket.error:
            data2 = prevdata2

        d2 = str(data2).split(',')

        try:
            data3 = s3.recv(1024).decode("utf-8")
            prevdata3 = data3
            countC+=1
        except socket.error:
            data3 = prevdata3

        d3 = str(data3).split(',')

        try:
            data4 = s4.recv(1024).decode("utf-8")
            prevdata4 = data4
            countB+=1
        except socket.error:
            data4 = prevdata4

        d4 = str(data4).split(',')

        try:
            data5 = s5.recv(1024).decode("utf-8")
            prevdata5 = data5
            countA+=1
        except socket.error:
            data5 = prevdata5

        d5 = str(data5).split(',')

        try:
            data6 = s6.recv(1024).decode("utf-8")
            prevdata6 = data6
            countG+=1
        except socket.error:
            data6 = prevdata6

        d6 = str(data6).split(',')

        try:
            data7 = s7.recv(1024).decode("utf-8")
            prevdata7 = data7
            countN+=1
        except socket.error:
            data7 = prevdata7

        d7 = str(data7).split(',')

        count+=1

        if prevaccD>0 and float(d3[gravaccz])<=0 and float(d3[Pitch])>0:
            nD -= 1
        elif prevaccD>0 and float(d3[gravaccz])<=0 and float(d3[Pitch])<0:
            nD += 1
        elif prevaccD<=0 and float(d3[gravaccz])>0 and float(d3[Pitch])>0:
            nD += 1
        elif prevaccD<=0 and float(d3[gravaccz])>0 and float(d3[Pitch])<0:
            nD -= 1


        prevaccD = float(d3[gravaccz])
        # print(nD,d3[Pitch],prevaccD,d3[az])
        d3[Pitch] = nD*180 + math.pow(-1,nD)*float(d3[Pitch])



        if prevaccN>0 and float(d4[gravaccz])<=0 and float(d4[Pitch])>0:
            nN -= 1
        elif prevaccN>0 and float(d4[gravaccz])<=0 and float(d4[Pitch])<0:
            nN += 1
        elif prevaccN<=0 and float(d4[gravaccz])>0 and float(d4[Pitch])>0:
            nN += 1
        elif prevaccN<=0 and float(d4[gravaccz])>0 and float(d4[Pitch])<0:
            nN -= 1
            
            
        prevaccN = float(d4[gravaccz])
        # print(nN,d4[Pitch],prevaccN,d4[az])
        d7[Pitch] = nN*180 + math.pow(-1,nN)*float(d4[Pitch])

        if prevaccG>0 and float(d4[gravaccz])<=0 and float(d4[Pitch])>0:
            nG -= 1
        elif prevaccG>0 and float(d4[gravaccz])<=0 and float(d4[Pitch])<0:
            nG += 1
        elif prevaccG<=0 and float(d4[gravaccz])>0 and float(d4[Pitch])>0:
            nG += 1
        elif prevaccG<=0 and float(d4[gravaccz])>0 and float(d4[Pitch])<0:
            nG -= 1
            
            
        prevaccG = float(d4[gravaccz])
        # print(nG,d4[Pitch],prevaccG,d4[az])
        d6[Pitch] = nG*180 + math.pow(-1,nG)*float(d4[Pitch])


        if countD <= 500:
            sumD+=float(d3[Pitch])
            if countD == 500:
                initial_calD = sumD/countD
                print("D calibration over")
        if countG <= 500:
            sumG+=float(d6[Pitch])
            if countG == 500:
                initial_calG = sumG/countG
                print("G calibration over")
        if countN <= 500:
            sumN+=float(d7[Pitch])
            if countN == 500:
                initial_calN = sumN/countN
                print("N calibration over")

        print("D6",d6[Pitch])
        if abs(float(d6[Pitch])-initial_calG)>60 and countG>500:
            reach_out1 = "reach_out"
            # print("Reach1", reach_out1)
        elif abs(float(d6[Pitch]) - initial_calG) < 60 and countG>500:
            reach_out1 = ""
        # if abs(float(d[Pitch])-initial_cal)>60 and count>500:
        #     reach_out2 = "reach_out"
        #     print("Reach2", reach_out2)
        # elif abs(float(d[Pitch]) - initial_cal) < 60 and count>500:
        #     reach_out2 = ""
        print("D7",d7[Pitch])
        if abs(float(d7[Pitch])-initial_calN)>30 and countN>500:
            step_out = "step_out"
            print("step", step_out)
        elif abs(float(d7[Pitch]) - initial_calN) < 30 and countN>500:
            step_out = ""
        print("D3",d3[Pitch])
        if abs(float(d3[Pitch])-initial_calD)>30 and countD>500:
            forward = "front"
            print("forward", forward)
        elif abs(float(d3[Pitch]) - initial_calD) <- 30 and countD>500:
            forward = "back"
        elif abs(float(d3[Pitch]) - initial_calD) < 30 and countD>500:
            forward = ""
        
        if reach_out1=="reach_out" or reach_out2=="reach_out":
            reach_out = "reach_out"
            print("Reach", reach_out)
        else:
            reach_out = ""

        # for i in game_data:
        #     game_data_str = game_data_str + str(i) + ','
        # game_data_str.strip(',')
        # game.write(str(sample_count)+','+str(time.time()) + ',' + str(port) + ',' +str(threadname).split(',')[0].split('(')[1] + str(game_data_str))
        
        if count>500:
            if forward!="":
                if reach_out!="" and step_out!="":
                    pose_detect = step_out+" "+reach_out+" "+forward
                elif reach_out!="":
                    pose_detect = reach_out+" "+forward
                else:
                    pose_detect = step_out+" "+forward
            elif forward=="":
                if reach_out!="" and step_out!="":
                    pose_detect = step_out+" "+reach_out
                elif reach_out!="":
                    pose_detect = reach_out
                else:
                    pose_detect = step_out
            print(pose_detect)
            sock.sendto(pose_detect.encode(),(UDP_IP, UDP_PORT))
            # sock.sendto("reach_out".encode(), (UDP_IP, UDP_PORT))


        
        
        file.write(str(data1)+','+str(data2)+','+str(data3)+','+str(data4)+','+str(data5)+','+str(data6)+','+str(data7)+','+str(rate)+','+str(time.time())+'\n')