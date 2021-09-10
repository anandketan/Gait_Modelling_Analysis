from threading import Thread
import time
import socket
import datetime
count =0
s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0",9999))

s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s2.bind(("0.0.0.0",8888))

s3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s3.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s3.bind(("0.0.0.0",7777))

s4 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s4.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s4.bind(("0.0.0.0",6666))

# s5 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s5.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s5.bind(("0.0.0.0",5555))
#
# s6 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s6.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s6.bind(("0.0.0.0",4444))

filename1 = input('Enter your name to be saved\n')
initial = 0
with open(filename1 + '.csv', 'w') as fp1:
   fp1.write('AccX1,AccY1,AccZ1,GyroX1,GyroY1,GyroZ1,1Q1, 1Q2, 1Q3, 1Q4, 1Roll,1Pitch,1Yaw,1count,1time,AccX2,AccY2,AccZ2,GyroX2,GyroY2,GyroZ2,2Q1, 2Q2, 2Q3, 2Q4, 2Roll,2Pitch,2Yaw,2count,2time,AccX3,AccY3,AccZ3,GyroX3,GyroY3,GyroZ3,3Q1, 3Q2, 3Q3, 3Q4, 3Roll,3Pitch,3Yaw,3count,3time,AccX4,AccY4,AccZ4,GyroX4,GyroY4,GyroZ4,4Q1, 4Q2, 4Q3, 4Q4, 4Roll,4Pitch,4Yaw,4count,4time,DATA_RATE\n')#AccX1,AccY1,AccZ1,GyroX1,GyroY1,GyroZ1,MagX1,MagY1,MagY1,Roll1,Pitch1,Yaw1,qw1,qx1,qy1,qz1,pressure sensor1,count1,time1,AccX2,AccY2,AccZ2,GyroX2,GyroY2,GyroZ2,MagX2,MagY2,MagY2,Roll2,Pitch2,Yaw2,qw2,qx2,qy2,qz2,pressuresensor2,count,time'+'\n')
# AccX5,AccY5,AccZ5,GyroX5,GyroY5,GyroZ5,5Q1, 5Q2, 5Q3, 5Q4, 5Roll,5Pitch,5Yaw,5count,5time,AccX6,AccY6,AccZ6,GyroX6,GyroY6,GyroZ6,6Q1, 6Q2, 6Q3, 6Q4, 6Roll,6Pitch,6Yaw,6count,6time,
   # fp1.write('AccX1,AccY1,AccZ1,GyroX1,GyroY1,GyroZ1,Roll1,Pitch1,Yaw1,qw1,qx1,qy1,qz1,pressure sensor1,count1,time1,AccX2,AccY2,AccZ2,GyroX2,GyroY2,GyroZ2,MagX2,MagY2,MagY2,Roll2,Pitch2,Yaw2,qw2,qx2,qy2,qz2,pressuresensor2,count,time'+'\n')')
   data1 = s1.recv(1024).decode("utf-8")
   data2 = s2.recv(1024)
   data3 = s3.recv(1024)
   data4 = s4.recv(1024)
   # data5 = s5.recv(1024)
   # data6 = s6.recv(1024)
   rate =0
   while True:
      if (count%100)==0:
         cur_time=time.time()
      if (count%100)==99:
         rate=99/(time.time()-cur_time)
      data1 = s1.recv(1024).decode("utf-8")
      data2 = s2.recv(1024)
      data3 = s3.recv(1024)
      data4 = s4.recv(1024)
      # data5 = s5.recv(1024)
      # data6 = s6.recv(1024)
      fp1.write(str(data1)+','+str(data2)+','+str(data3)+','+str(data4)+','+ str(rate)+'\n')
      # +str(data5)+','+str(data6)+
      count+=1
      d1 = str(data1).split(',')
      d2 = str(data2).split(',')
      d3 = str(data3).split(',')
      d4 = str(data4).split(',')
      # d5 = str(data5).split(',')
      # d6 = str(data6).split(',')
      # initial = 0
      if count == 1:
         print(count)
         initial1 = int(d1[-2]) - count - 1
         initial2 = int(d2[-2]) - count - 1
         initial3 = int(d3[-2]) - count - 1
         initial4 = int(d4[-2]) - count - 1
         # initial5 = int(d5[-2]) - count - 1
         # initial6 = int(d6[-2]) - count - 1
      print(initial1, int(d1[-2]))
      print(initial2, int(d2[-2]))
      print(initial3, int(d3[-2]))
      print(initial4, int(d4[-2]))
      # print(initial5, int(d5[-2]))
      # print(initial6, int(d6[-2]))
      print('d1', d1[-5:-1], "Received:", count-1, "Data rate:",rate,"Drop:",int(d1[-2])-count-1-initial1)
      print('d2', d2[-5:-1], "Received:", count-1, "Data rate:",rate,"Drop:",int(d2[-2])-count-1-initial2)
      print('d3', d3[-5:-1], "Received:", count-1, "Data rate:",rate,"Drop:",int(d3[-2])-count-1-initial3)
      print('d4', d4[-5:-1], "Received:", count-1, "Data rate:",rate,"Drop:",int(d4[-2])-count-1-initial4)
      # print('d5', d5[-5:-1], "Received:", count-1, "Data rate:",rate,"Drop:",int(d5[-2])-count-1-initial5)
      # print('d6', d6[-5:-1], "Received:", count-1, "Data rate:",rate,"Drop:",int(d6[-2])-count-1-initial6)
##    if KeyboardInterrupt:
##       s.close()
##       print "Socket Closed"
