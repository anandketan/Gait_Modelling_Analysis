from threading import Thread
import time
import socket
import datetime
import keyboard

count =0
s1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0",9999))
s2 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s2.bind(("0.0.0.0",8888))
# s3 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s3.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s3.bind(("0.0.0.0",7777))
s4 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s4.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s4.bind(("0.0.0.0",6666))
s5 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s5.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s5.bind(("0.0.0.0",5555))
# s6 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s6.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s6.bind(("0.0.0.0",4444))
# s7 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s7.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s7.bind(("0.0.0.0",3333))

filename1 = input('Enter your name to be saved\n')
with open(filename1 + '.csv', 'w') as fp1:
   print("Here")
   fp1.write('AccX,AccY,AccZ,GyroX,GyroY,GyroZ,Q1,Q2,Q3,Q4,QYaw,QPitch,QRoll,Yaw,Pitch,Roll,count1,imu_time1,hs1,distance,2AccX,2AccY,2AccZ,2GyroX,2GyroY,2GyroZ,2Q1,2Q2,2Q3,2Q4,2QYaw,2QPitch,2QRoll,2Yaw,2Pitch,2Roll,count2,imu_time2,hs2,distance2,3AccX,3AccY,3AccZ,3GyroX,3GyroY,3GyroZ,3Q1,3Q2,3Q3,3Q4,3QYaw,3QPitch,3QRoll,3Yaw,3Pitch,3Roll,count3,imu_time3,hs3,distance3,4AccX,4AccY,4AccZ,4GyroX,4GyroY,4GyroZ,4Q1,4Q2,4Q3,4Q4,4QYaw,4QPitch,4QRoll,4Yaw,4Pitch,4Roll,count4,imu_time4,hs4,distance4,5AccX,5AccY,5AccZ,5GyroX,5GyroY,5GyroZ,5Q1,5Q2,5Q3,5Q4,5QYaw,5QPitch,5QRoll,5Yaw,5Pitch,5Roll,count5,imu_time5,hs5,distance5,6AccX,6AccY,6AccZ,6GyroX,6GyroY,6GyroZ,6Q1,6Q2,6Q3,6Q4,6QYaw,6QPitch,6QRoll,6Yaw,6Pitch,6Roll,count6,imu_time6,hs6,distance6,7AccX,7AccY,7AccZ,7GyroX,7GyroY,7GyroZ,7Q1,7Q2,7Q3,7Q4,7QYaw,7QPitch,7QRoll,7Yaw,7Pitch,7Roll,count7,imu_time7,hs7,distance7,rate,receiver_time,heel_strike\n')#AccX1,AccY1,AccZ1,GyroX1,GyroY1,GyroZ1,MagX1,MagY1,MagY1,Roll1,Pitch1,Yaw1,qw1,qx1,qy1,qz1,pressure sensor1,count1,time1,AccX2,AccY2,AccZ2,GyroX2,GyroY2,GyroZ2,MagX2,MagY2,MagY2,Roll2,Pitch2,Yaw2,qw2,qx2,qy2,qz2,pressuresensor2,count,time'+'\n')
   data1 = s1.recv(1024).decode("utf-8")
   data2 = s2.recv(1024).decode("utf-8")
#    data3 = s3.recv(1024).decode("utf-8")
   data4 = s4.recv(1024).decode("utf-8")
   data5 = s5.recv(1024).decode("utf-8")
#    data6 = s6.recv(1024).decode("utf-8")
#    data7 = s7.recv(1024).decode("utf-8")
   rate =0
   while True:
      if (count%100)==0:
         cur_time=time.time()
      if (count%100)==99:
         rate=99/(time.time()-cur_time)
      data1 = s1.recv(1024).decode("utf-8")
      data2 = s2.recv(1024).decode("utf-8")
    #   data3 = s3.recv(1024).decode("utf-8")
      data4 = s4.recv(1024).decode("utf-8")
      data5 = s5.recv(1024).decode("utf-8")
    #   data6 = s6.recv(1024).decode("utf-8")
    #   data7 = s7.recv(1024).decode("utf-8")
      if (keyboard.is_pressed("q")):
         hs =100
      else:
         hs=0
    #   fp1.write(str(data1)+','+str(data2)+','+str(data3)+','+str(data4)+','+str(data5)+','+str(data6)+','+str(data7)+','+ str(rate)+','+str(time.time())+','+ str(hs)+'\n')
      fp1.write(str(data1)+','+str(data2)+','+str(data4)+','+str(data5)+','+ str(rate)+','+str(time.time())+','+ str(hs)+'\n')
      count+=1
      d= str(data1).split(',')
      print(d[-5:-2], "Received:", count-1, "Data rate:",rate)
##    if KeyboardInterrupt:
##       s.close()
##       print "Socket Closed"
