import threading
from threading import Thread
import time
import socket
import datetime
from datetime import datetime
import signal
import os

file_name_flag_combined = 'combined_data_flagged.csv'
file_name_combined = 'combined_data.csv'
file_name_game = 'game_data.csv'
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'GameDataFolder', '{}_{}_{}_{}'.format(datetime.now().date(), datetime.now().time().hour, datetime.now().time().minute, datetime.now().time().second))
try:
    os.makedirs(dest_dir)
except OSError:
    pass # already exists
path_flag_combined = os.path.join(dest_dir, file_name_flag_combined)
path_combined = os.path.join(dest_dir, file_name_combined)
path_game = os.path.join(dest_dir, file_name_game)


try:
    collect_time = int(input("Enter time in seconds to collect data\n"))
except:
    collect_time = 60


try:
    forearm_port = int(input('Enter port number of sensor attached to forearm\n'))
except:
    forearm_port = 9999

try:
    bicep_port = int(input('Enter port number of sensor attached to bicep\n'))
except:
    bicep_port = 8888

try:
    thigh_port = int(input('Enter port number of sensor attached to thigh\n'))
except:
    thigh_port = 7777

port1 = 9999
filename1 = input('Enter filename for sensor(E) connected on port {}\n'.format(port1))
path1 = os.path.join(dest_dir, filename1+'_sensorE.csv')
# exit_event1 = threading.Event()
port2 = 8888
filename2 = input('Enter filename for sensor(D) connected on port {}\n'.format(port2))
path2 = os.path.join(dest_dir, filename2+'_sensorD.csv')

port3 = 7777
filename3 = input('Enter filename for sensor(C) connected on port {}\n'.format(port3))
path3 = os.path.join(dest_dir, filename3+'_sensorC.csv')

port4 = 6666
filename4 = input('Enter filename for sensor(B) connected on port {}\n'.format(port4))
path4 = os.path.join(dest_dir, filename4+'_sensorB.csv')

port5 = 5555
filename5 = input('Enter filename for sensor(A) connected on port {}\n'.format(port5))
path5 = os.path.join(dest_dir, filename5+'_sensorA.csv')

port6 = 4444
filename6 = input('Enter filename for sensor(G) connected on port {}\n'.format(port6))
path6 = os.path.join(dest_dir, filename6+'_sensorG.csv')

port7 = 3333
filename7 = input('Enter filename for sensor(N) connected on port {}\n'.format(port7))
path7 = os.path.join(dest_dir, filename7+'_sensorN.csv')

flags = {9999:True, 8888:True, 7777:True, 6666:True, 5555:True, 4444:True, 3333:True}

UDP_IP ="192.168.100.2"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

pose_detect = ""
reach_out1 = ""
reach_out2 = ""
reach_out = ""
step_out = ""
roll = -3
pitch = -4
yaw = -5


with open(path_combined, 'w') as comb, open(path_flag_combined, 'w') as comb_flag:
    comb.write('update#,yaw9, pitch9, roll9,yaw8, pitch8, roll8,yaw7, pitch7, roll7,yaw6, pitch6, roll6,yaw5, pitch5, roll5,yaw4, pitch4, roll4,yaw3, pitch3, roll3, Thread, port, time,rate\n')
    comb_flag.write('update#,yaw9, pitch9, roll9,yaw8, pitch8, roll8,yaw7, pitch7, roll7,yaw6, pitch6, roll6,yaw5, pitch5, roll5,yaw4, pitch4, roll4,yaw3, pitch3, roll3, , Thread, port, time,rate\n')

with open(path_game, 'w') as game:
    game.write('update#,time, port, thread, Reach_out, Step_out\n')

all_data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
game_data = [0,0]
sample_count = 0
flag_sample_count = 0


class camThread(threading.Thread):
    def __init__(self, port, filename):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.setblocking(0)
        self.filename = filename
        self.lock = threading.Lock()
        self.exit_event = threading.Event()
        self.port = port

    def run(self):
        print("Starting on port", self.port)
        data_receive(self, self.filename, self.sock, self.lock, self.exit_event, self.port)


def data_receive(threadname, filename, sock, lock, exit_event, port):
    global reach_out2
    global reach_out
    global reach_out1
    global step_out
    global pose_detect

    global all_data
    global game_data
    global sample_count
    global flag_sample_count

    global flags

    lock.acquire()
    count = 0
    rate = 0
    initial = 0
    sum=0.0
    initial_cal = 0

    with open(filename,'w') as fp, open (path_combined,'a') as comb, open (path_game,'a') as game, open(path_flag_combined, 'w') as comb_flag:
        fp.write('AccX,AccY,AccZ,GyroX,GyroY,GyroZ,Q1, Q2, Q3, Q4, Yaw,Pitch,Roll,count,imu_time,receiver_time,DATA_RATE\n')
        # print("{} has entered here at {}".format(threadname, datetime.now().time()))
        start = time.time()
        try:
            # print("{} has entered here at {}".format(threadname, datetime.now().time()))
            while time.time() - start < collect_time:
                # print("{} has entered here at {}".format(threadname, datetime.now().time()))
                flags[port] = True
                try:
                    data = sock.recv(1024).decode("utf-8")
                except socket.error:
                    continue

                sample_count+=1
                all_data_str = ""
                game_data_str = ""
                
                if (count % 100) == 0:
                    cur_time = time.time()
                if (count % 100) == 99:
                    rate = 99 / (time.time() - cur_time)

                fp.write(str(data) + ',' + str(time.time()) + ',' + str(rate) + '\n')
                # fp.write(str(count)+','+ str(datetime.now().time())+','+ str(rate)+'\n')
                count += 1
                
                d = str(data).split(',')
                if port==9999:
                    all_data[0:3] = d[-5:-2]
                if port==8888:
                    all_data[3:6] = d[-5:-2]
                if port==7777:
                    all_data[6:9] = d[-5:-2]
                if port==6666:
                    all_data[9:12] = d[-5:-2]
                if port==5555:
                    all_data[12:15] = d[-5:-2]
                if port==4444:
                    all_data[15:18] = d[-5:-2]
                if port == 3333:
                    all_data[18:] = d[-5:-2]
                for i in all_data:
                    all_data_str = all_data_str + str(i) + ','
                all_data_str.strip(',')
                
                if (sample_count%100)==0:
                    cur_comb_time=time.time()
                if (sample_count%100)==99:
                    comb_rate=100/(time.time()-cur_comb_time)
                comb.write(str(sample_count)+','+str(all_data_str) + ',' +str(threadname).split(',')[0].split('(')[1] + ',' + str(port) + ',' + str(time.time())+ ',' + str(comb_rate))

                if all(value == True for value in flags.values()):
                    if (flag_sample_count%100)==0:
                        cur_comb_flag_time=time.time()
                    if (flag_sample_count%100)==99:
                        comb_flag_rate=100/(time.time()-cur_comb_flag_time)
                    flag_sample_count+=1
                    comb_flag.write(str(flag_sample_count)+','+str(all_data_str) + ',' +str(threadname).split(',')[0].split('(')[1] + ',' + str(port) + ',' + str(time.time())+ ',' + str(comb_flag_rate)+'\n')
                    for key, value in flags.items():
                        flags[key]=False

                if port == forearm_port and count <= 500:
                    sum+=float(d[roll])
                    if count == 500:
                        initial_cal = sum/count
                        # print("Port 8888 cal over", initial_cal)
                if port == bicep_port and count <= 500:
                    sum+=float(d[roll])
                    if count == 500:
                        initial_cal = sum/count
                        # print("Port 7777 cal over", initial_cal)
                if port == thigh_port and count <= 500:
                    sum+=float(d[pitch])
                    if count == 500:
                        initial_cal = sum/count
                        # print("Port 6666 cal over", initial_cal)
                if count == 1:
                    print(count)
                    initial = int(d[-2]) - count - 1
                # print(initial, int(d[-2]))
                # print(d[-5:-1], " Received:", count - 1, " Data rate:", rate, " Drop:",
                #       int(d[-2]) - count - 1 - initial, " Port:", port)
                # print("count:", count, "Rate:", rate)
                # print(port, ":", abs(float(d[-3])-initial_cal))
                # print(port, ":", abs(float(d[-4]) - initial_cal))
                if port == forearm_port and abs(float(d[roll])-initial_cal)>60 and count>500:
                    reach_out1 = "reach_out"
                    print("Reach1", reach_out1)
                elif port == forearm_port and abs(float(d[roll]) - initial_cal) < 60 and count>500:
                    reach_out1 = ""
                if port == bicep_port and abs(float(d[roll])-initial_cal)>60 and count>500:
                    reach_out2 = "reach_out"
                    print("Reach2", reach_out2)
                elif port == bicep_port and abs(float(d[roll]) - initial_cal) < 60 and count>500:
                    reach_out2 = ""
                if port == thigh_port and abs(float(d[pitch])-initial_cal)>60 and count>500:
                    step_out = "step_out"
                    game_data[1] = 1
                    print("step", step_out)
                elif port == thigh_port and abs(float(d[pitch]) - initial_cal) < 60 and count>500:
                    game_data[1] = 0
                    step_out = ""
                
                if reach_out1=="reach_out" and reach_out2=="reach_out":
                    reach_out = "reach_out"
                    game_data[0] = 1
                    print("Reach", reach_out)
                else:
                    reach_out = ""
                    game_data[0] = 0

                for i in game_data:
                    game_data_str = game_data_str + str(i) + ','
                game_data_str.strip(',')
                game.write(str(sample_count)+','+str(time.time()) + ',' + str(port) + ',' +str(threadname).split(',')[0].split('(')[1] + str(game_data_str))
                
                if count>500:
                    if reach_out!="" and step_out!="":
                        pose_detect = step_out+" "+reach_out
                    elif reach_out!="":
                        pose_detect = reach_out
                    else:
                        pose_detect = step_out
                    print(pose_detect)
                    sock.sendto(pose_detect.encode(),(UDP_IP, UDP_PORT))
                    # sock.sendto("reach_out".encode(), (UDP_IP, UDP_PORT))
                
                if exit_event.is_set():
                    break
        except Exception as e:
            print(e)
        finally:
            # print("{} has entered here at {}".format(threadname, datetime.now().time()))
            sock.close()
    lock.release()


lock = threading.Lock()
thread1 = camThread(port1, filename1)
thread2 = camThread(port2, filename2)
thread3 = camThread(port3, filename3)
thread4 = camThread(port4, filename4)
thread5 = camThread(port5, filename5)
thread6 = camThread(port6, path6)
thread7 = camThread(port7, path7)
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
print("Time up!!!!!!!!!!!!!!!!!!!!!")