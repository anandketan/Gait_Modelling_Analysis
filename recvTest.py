import socket
import time


def listenfordata(sensor):
    try:
        data[sensor] = socks[sensor].recv(1024).decode("utf-8")
        if count[sensor] == 0:
            initialtime[sensor] = time.time()
        count[sensor] += 1
        if time.time() - initialtime[sensor] > 1:
            rate[sensor] = round(count[sensor] / (time.time() - initialtime[sensor]), 2)
            count[sensor] = 0
    except socket.error:
        if time.time() - initialtime[sensor] > 10:
            rate[sensor] = 0
            count[sensor] = 0


noOfDevices = 9
device_list = ['E', 'D', 'C', 'B', 'A', 'G', 'N', 'F', 'H']
port_list = [9999, 8888, 7777, 6666, 5555, 4444, 3333, 9000, 8000]

count = {}
initialtime = {}
rate = {}
data = {}

for device in device_list:
    count[device] = 0
    initialtime[device] = 0.0
    rate[device] = 0.0
    if device != 'E':
        data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
    else:
        data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(noOfDevices)]
for port, sock in zip(port_list, sock_list):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    sock.setblocking(0)

socks = {}
for device, sock in zip(device_list, sock_list):
    socks[device] = sock

while True:
    for sensor in device_list:
        listenfordata(sensor)
    print({x: rate[x] for x in rate if rate[x] > 0})
    # print(rate)
