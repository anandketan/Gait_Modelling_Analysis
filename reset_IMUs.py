import socket

HOST = "0.0.0.0"
IP, PORT = "192.168.1.188",7777
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
while True:
    sock.sendto("reset".encode(), (IP,PORT))