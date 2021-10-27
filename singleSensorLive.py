import matplotlib.pyplot as plt
import numpy as np
import socket

s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s1.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s1.bind(("0.0.0.0", 8888))

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

plt.style.use('ggplot')
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
#  * remember to change the range for better real-time visualization *
ax.set_ylim([-360, 360])
line1, = ax.plot(x, y1, 'b-', label='yaw')
line2, = ax.plot(x, y2, 'r-', label='pitch')
line3, = ax.plot(x, y3, 'y-', label='roll')

#  update => graph refreshes itself after every 'r' number of received values
#  increasing 'r', decreases refresh rate and latency between sensor movement & graph change
#  decreasing 'r', increases refresh rate but latency increases
r = 20

k = 0
while True:
    data1 = s1.recv(1024).decode("utf-8")
    d = str(data1).split(',')
    print(d[-3])
    y1 = np.roll(y1, -1)
    y1[-1] = d[-3]
    y2 = np.roll(y2, -1)
    y2[-1] = d[-6]
    y3 = np.roll(y3, -1)
    y3[-1] = 0
    print(k)
    k = k + 1
    if k == r:
        line1.set_ydata(y1)
        line2.set_ydata(y2)
        line3.set_ydata(y3)
        fig.canvas.draw()
        fig.canvas.flush_events()
        k = 0