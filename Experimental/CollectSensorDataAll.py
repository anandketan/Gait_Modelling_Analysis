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
prevdata2 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata3 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata4 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata5 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata6 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata7 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

filename1 = input('Enter your name to be saved\n')
with open(filename1 + '.csv', 'w') as fp1:
   rate =0
   while True:
      if (count%100)==0:
         cur_time=time.time()
      if (count%100)==99:
         rate=99/(time.time()-cur_time)
      
      try:
         data1 = s1.recv(1024).decode("utf-8")
         prevdata1 = data1
      except socket.error:
         data1 = prevdata1

      try:
         data2 = s2.recv(1024).decode("utf-8")
         prevdata2 = data2
      except socket.error:
         data2 = prevdata2

      try:
         data3 = s3.recv(1024).decode("utf-8")
         prevdata3 = data3
      except socket.error:
         data3 = prevdata3

      try:
         data4 = s4.recv(1024).decode("utf-8")
         prevdata4 = data4
      except socket.error:
         data4 = prevdata4

      try:
         data5 = s5.recv(1024).decode("utf-8")
         prevdata5 = data5
      except socket.error:
         data5 = prevdata5

      try:
         data6 = s6.recv(1024).decode("utf-8")
         prevdata6 = data6
      except socket.error:
         data6 = prevdata6

      try:
         data7 = s7.recv(1024).decode("utf-8")
         prevdata7 = data7
      except socket.error:
         data7 = prevdata7

      if (keyboard.is_pressed("q")):
         hs =100
      else:
         hs=0
      
      fp1.write(str(data1)+','+str(data2)+','+str(data3)+','+str(data4)+','+str(data5)+','+str(data6)+','+str(data7)+','+ str(rate)+','+str(time.time())+','+ str(hs)+'\n')
      count+=1
      print("Received:", count-1, "Data rate:",rate)
