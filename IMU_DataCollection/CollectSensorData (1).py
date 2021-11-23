from threading import Thread
import time
import socket
import datetime
count =0;
s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0",7777))
# s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s2.bind(("0.0.0.0",9992))
# s3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s3.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s3.bind(("0.0.0.0",9993))
filename1 = input('Enter your name to be saved\n')
initial = 0
with open(filename1 + '.csv', 'w') as fp1:
   fp1.write('AccX,AccY,AccZ,GyroX,GyroY,GyroZ,Q1, Q2, Q3, Q4, Roll,Pitch,Yaw,count,time,DATA_RATE\n')#AccX1,AccY1,AccZ1,GyroX1,GyroY1,GyroZ1,MagX1,MagY1,MagY1,Roll1,Pitch1,Yaw1,qw1,qx1,qy1,qz1,pressure sensor1,count1,time1,AccX2,AccY2,AccZ2,GyroX2,GyroY2,GyroZ2,MagX2,MagY2,MagY2,Roll2,Pitch2,Yaw2,qw2,qx2,qy2,qz2,pressuresensor2,count,time'+'\n')
   data1 = s1.recv(1024).decode("utf-8")
   # data2 = s2.recv(1024)
   # data3 = s3.recv(1024)
   rate =0
   while True:
      if (count%100)==0:
         cur_time=time.time()
      if (count%100)==99:
         rate=99/(time.time()-cur_time)
      data1 = s1.recv(1024).decode("utf-8")
      # data2 = s2.recv(1024)
      # data3 = s3.recv(1024)
      fp1.write(str(data1)+','+ str(rate)+'\n')
      count+=1
      d= str(data1).split(',')
      # initial = 0
      if count == 1:
         print(count)
         initial = int(d[-2]) - count - 1
      print(initial, int(d[-2]))
      print(d[-5:-1], "Received:", count-1, "Data rate:",rate,"Drop:",int(d[-2])-count-1-initial)
##    if KeyboardInterrupt:
##       s.close()
##       print "Socket Closed"
