import matplotlib.pyplot as plt
import numpy as np
import socket
import time

def correctYaw(prevyaw, yaw, n):
    if prevyaw >= 170 and prevyaw <=180 and float(yaw) >=-180 and float(yaw) <=-170:
        n += 1
    elif float(yaw) >= 170 and float(yaw) <=180 and prevyaw >=-180 and prevyaw <=-170:
        n -= 1

    prevyawnew = float(yaw)
    # print(nC, pitch, prevaccC, d3[az])
    yawnew = n * 360 + float(yaw)
    return prevyawnew, yawnew, n

def correctRoll(prevroll, roll, n):
    if prevroll >= 170 and prevroll <=180 and float(roll) >=-180 and float(roll) <=-170:
        n += 1
    elif float(roll) >= 170 and float(roll) <=180 and prevroll >=-180 and prevroll <=-170:
        n -= 1

    prevrollnew = float(roll)
    # print(nC, pitch, prevaccC, d3[az])
    rollnew = n * 360 + float(roll)
    return prevrollnew, rollnew, n

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0", 8888))
# s1.setblocking(0)
#
# s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# s2.bind(("0.0.0.0", 9999))
# s2.setblocking(0)

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
sys = 23
gyro = 24
accel = 25
mag = 26

#  display_values => number of values to display at once on the plot
display_values = 200
x = np.linspace(0, display_values, display_values)
y3 = np.zeros(display_values)
y2 = np.zeros(display_values)
y1 = np.zeros(display_values)
y4 = np.zeros(display_values)
y5 = np.zeros(display_values)
y6 = np.zeros(display_values)
y7 = np.zeros(display_values)
y8 = np.zeros(display_values)
y9 = np.zeros(display_values)

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-360, 360])
line1, = ax.plot(x, y1, label='accX')
line2, = ax.plot(x, y2, label='accY')
line3, = ax.plot(x, y3, label='accZ')
line4, = ax.plot(x, y4, label='gyroX')
line5, = ax.plot(x, y5, label='gyroY')
line6, = ax.plot(x, y6, label='gyroZ')
line7, = ax.plot(x, y7, label='magX')
line8, = ax.plot(x, y8, label='magY')
line9, = ax.plot(x, y9, label='magZ')

ax.legend()

#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 30

k = 0
counter = 0
rate = 0

nCyaw = 0
prevyawC = 0
nCroll = 0
prevrollC = 0
while True:
    data1 = s1.recv(256).decode("utf-8")
    if counter == 0:
        initialtime = time.time()
    counter+=1
    if time.time() - initialtime > 1:
        rate = counter / (time.time() - initialtime)
        # print(rate, time.time() - initialtime, counter)
        counter = 0
    print(rate)
    d = str(data1).split(',')
    # # print(d[calcPitch])
    # # prevyawC, d[calcYaw], nCyaw = correctYaw(prevyawC, d[calcYaw], nCyaw)
    # # prevrollC, d[calcRoll], nCroll = correctRoll(prevrollC, d[calcRoll], nCroll)
    # # data2 = s2.recv(1024).decode("utf-8")
    # # d2 = str(data2).split(',')
    # # print(d[-3])
    y1 = np.roll(y1, -1)
    y1[-1] = float(d[0])
    y2 = np.roll(y2, -1)
    y2[-1] = float(d[1])
    y3 = np.roll(y3, -1)
    y3[-1] = float(d[2])
    y4 = np.roll(y4, -1)
    y4[-1] = float(d[gx])
    y5 = np.roll(y5, -1)
    y5[-1] = float(d[gy])
    y6 = np.roll(y6, -1)
    y6[-1] = float(d[gz])
    y7 = np.roll(y7, -1)
    y7[-1] = float(d[-3])
    y8 = np.roll(y8, -1)
    y8[-1] = float(d[-2])
    y9 = np.roll(y9, -1)
    y9[-1] = float(d[calcRoll])
    # # print(k)
    k = k + 1
    if k == r:
        # line1.set_ydata(y1)
        # line2.set_ydata(y2)
        # line3.set_ydata(y3)
        # line4.set_ydata(y4)
        # line5.set_ydata(y5)
        # line6.set_ydata(y6)
        # line7.set_ydata(y7)
        # line8.set_ydata(y8)
        line9.set_ydata(y9)
        fig.canvas.draw()
        fig.canvas.flush_events()
        k = 0