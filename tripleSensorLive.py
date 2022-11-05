import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import utils_sensor_data as utils

sens1, port1 = 'H', 8000
sens2, port2 = 'N', 3333
sens3, port3 = 'F', 9000

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0", port1))
s1.setblocking(0)

s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s2.bind(("0.0.0.0", port2))
s2.setblocking(0)

s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s3.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s3.bind(("0.0.0.0", port3))
s3.setblocking(0)

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

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-360, 360])
line1, = ax.plot(x, y1, label='{}-Roll'.format(sens1))
line2, = ax.plot(x, y2, label='{}-Pitch'.format(sens1))
line3, = ax.plot(x, y3, label='{}-Yaw'.format(sens1))
line4, = ax.plot(x, y4, label='{}-Roll'.format(sens2))
line5, = ax.plot(x, y5, label='{}-Pitch'.format(sens2))
line6, = ax.plot(x, y6, label='{}-Yaw'.format(sens2))
line7, = ax.plot(x, y7, label='{}-Roll'.format(sens3))
line8, = ax.plot(x, y8, label='{}-Pitch'.format(sens3))
line9, = ax.plot(x, y9, label='{}-Yaw'.format(sens3))

ax.legend()

#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 15

k = 0
counter = 0
rate = 0

n1yaw = 0
prevyaw1 = 0
n1roll = 0
prevroll1 = 0
n1pitch = 0
prevacc1 = 0

n2yaw = 0
prevyaw2 = 0
n2roll = 0
prevroll2 = 0
n2pitch = 0
prevacc2 = 0

n3yaw = 0
prevyaw3 = 0
n3roll = 0
prevroll3 = 0
n3pitch = 0
prevacc3 = 0

prevdata1 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata2 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
prevdata3 = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

while True:
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

    if counter == 0:
        initialtime = time.time()
    counter+=1
    if time.time() - initialtime > 1:
        rate = counter / (time.time() - initialtime)
        counter = 0
    print(rate)

    d1 = str(data1).split(',')
    prevyaw1, d1[calcYaw], n1yaw = utils.correctYaw(prevyaw1, d1[calcYaw], n1yaw)
    prevroll1, d1[calcRoll], n1roll = utils.correctRoll(prevroll1, d1[calcRoll], n1roll)
    # prevacc1, d1[calcPitch], n1pitch = utils.correctPitch(prevacc1, d1[gravaccy], d1[calcPitch], n1pitch)

    d2 = str(data2).split(',')
    prevyaw2, d2[calcYaw], n2yaw = utils.correctYaw(prevyaw2, d2[calcYaw], n2yaw)
    prevroll2, d2[calcRoll], n2roll = utils.correctRoll(prevroll2, d2[calcRoll], n2roll)
    # prevacc2, d2[calcPitch], n2pitch = utils.correctPitch(prevacc2, d2[gravaccy], d2[calcPitch], n2pitch)

    d3 = str(data3).split(',')
    prevyaw3, d3[calcYaw], n3yaw = utils.correctYaw(prevyaw3, d3[calcYaw], n3yaw)
    prevroll3, d3[calcRoll], n3roll = utils.correctRoll(prevroll3, d3[calcRoll], n3roll)
    # prevacc3, d3[calcPitch], n3pitch = utils.correctPitch(prevacc3, d3[gravaccy], d3[calcPitch], n3pitch)

    y1 = np.roll(y1, -1)
    y1[-1] = d1[calcRoll]

    y2 = np.roll(y2, -1)
    y2[-1] = d1[calcPitch]

    y3 = np.roll(y3, -1)
    y3[-1] = d1[calcYaw]

    y4 = np.roll(y4, -1)
    y4[-1] = d2[calcRoll]

    y5 = np.roll(y5, -1)
    y5[-1] = d2[calcPitch]

    y6 = np.roll(y6, -1)
    y6[-1] = d2[calcYaw]

    y7 = np.roll(y7, -1)
    y7[-1] = d3[calcRoll]

    y8 = np.roll(y8, -1)
    y8[-1] = d3[calcPitch]

    y9 = np.roll(y9, -1)
    y9[-1] = d3[calcYaw]

    k = k + 1
    if k == r:
        line1.set_ydata(y1)
        line2.set_ydata(y2)
        line3.set_ydata(y3)
        line4.set_ydata(y4)
        line5.set_ydata(y5)
        line6.set_ydata(y6)
        line7.set_ydata(y7)
        line8.set_ydata(y8)
        line9.set_ydata(y9)
        fig.canvas.draw()
        fig.canvas.flush_events()
        k = 0