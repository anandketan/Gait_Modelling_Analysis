import socket
import time

def listenfordata(sensor, location):
    try:
        data[sensor] = sockets[location].recv(1024).decode("utf-8")
        if count[sensor] == 0:
            initialtime[sensor] = time.time()
        count[sensor] += 1
        if time.time() - initialtime[sensor] > 1:
            rate[sensor] = round(count[sensor] / (time.time() - initialtime[sensor]), 2)
            count[sensor] = 0
    except socket.error:
        pass


device_list = ['D', 'C', 'B', 'F', 'H', 'G', 'N']
port_list = [8888, 7777, 6666, 9000, 8000, 4444, 3333]

count = {}
initialtime = {}
rate = {}
data = {}

for device in device_list:
    count[device] = 0
    initialtime[device] = 0
    rate[device] = 0
    data[device] = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"

print(data)

sock_list = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(5)]
for port, sock in zip(port_list, sock_list):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    sock.setblocking(0)

socks = {}
for device, sock in zip(device_list, sock_list):
    socks[device] = sock

sockets = {'right_bicep': socks['D'], 'right_thigh': socks['C'], 'right_shank': socks['B'], 'back': socks['F'],
           'right_forearm': socks['H']}



while True:
    for sensor, location in zip(device_list, sockets):
        listenfordata(sensor, location)
    print({x: rate[x] for x in rate if rate[x] > 0})
    print(rate)
