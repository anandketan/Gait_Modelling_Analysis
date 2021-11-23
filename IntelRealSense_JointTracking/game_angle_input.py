import cv2
import threading
from cv2 import aruco
import numpy as np
import math
import pandas as pd
import socket
import pyrealsense2 as rs
import numpy as np
from collections import deque
import time
from datetime import datetime
import csv

UDP_IP = "192.168.100.202"
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

backcameraid = "108322073108"
sidecameraid = "108322073120"
sidemarkers = [4,8]
backmarkers = [1,2]
allmarkers = backmarkers + sidemarkers

last = []
direction = ""
global_centroids = {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0), 7: (0, 0), 8: (0, 0),
                         9: (0, 0)}
forwardangle = 90
sidewaysangle = 90
overall_update = 0

previoussidewaysangle = 90
previousforwardangle = 90

maxleft = 0
maxright = 0
numberleft = 0
numberright = 0
numberforward = 0
numberbackward = 0
timeleft = 0
timeright = 0
chocolates = 0

filename = "thread_test.csv"
fields = ["overall_update","time", "forward angle", "sideways angle", "direction string", "updated by", "count for thread", "frame number for thread", "processing time"]

with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)

class camThread(threading.Thread):
    def __init__(self, previewName, camID, markerlist):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.lock = threading.Lock()
        self.markerlist = markerlist
    def run(self):
        print("Starting ", self.previewName)
        camPreview(self, self.previewName, self.camID, self.lock, self.markerlist)

def camPreview(threadname, previewName, camID, lock, markerlist):
    global direction
    global global_centroids
    global forwardangle
    global sidewaysangle
    global overall_update
    global filename
    global sidemarkers
    global backmarkers
    global maxleft
    global maxright
    global numberleft
    global numberright
    global numberforward
    global numberbackward
    global timeleft
    global timeright
    global chocolates
    lock.acquire()
    # print("{} has entered here at {}".format(threadname, datetime.now().time()))
    cv2.namedWindow(previewName)
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(camID)
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 60)
    pipeline.start(config)
    count = 1
    prev_centroids = {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0), 7: (0, 0), 8: (0, 0), 9: (0, 0)}
    c = np.array(np.zeros([9, 4, 2]))
    ids = [[1], [2], [3], [4], [5], [6], [7], [8], [9]]
    try:
        # print("{} has entered here at {}".format(threadname, datetime.now().time()))
        while cv2.getWindowProperty(previewName, 0) >= 0:
            # print("{} has entered here at {}".format(threadname, datetime.now().time()))
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            # depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue
            start = time.time()
            frame_number = frames.get_frame_number()
            # print("{}{}".format(threadname,frame_number))
            # print("{} has entered here at {}".format(threadname, datetime.now().time()))
            image = np.asanyarray(color_frame.get_data())
            #image = cv2.resize(color_image, (1200, 800))
            arucodict = aruco.Dictionary_get(aruco.DICT_6X6_50)
            arucoparams = aruco.DetectorParameters_create()
            (corners, id, rejected) = aruco.detectMarkers(image, arucodict, parameters=arucoparams)
            # print(id,corners)
            if id is not None:
                for (a, b) in zip(corners, id):
                    if b in range(0, 10):
                        c[b - 1] = a
            centroids = {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0), 7: (0, 0), 8: (0, 0),
                         9: (0, 0)}
            if len(corners) > 0:
                id = id.flatten()
                for (markerCorner, markerID) in zip(c, ids):
                    corners = markerCorner.reshape((4, 2))
                    (topLeft, topRight, bottomRight, bottomLeft) = corners
                    topRight = (int(topRight[0]), int(topRight[1]))
                    bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                    bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                    topLeft = (int(topLeft[0]), int(topLeft[1]))
                    # cv2.line(image, topLeft, topRight, (255, 0, 0), 5)
                    # cv2.line(image, topRight, bottomRight, (255, 0, 0), 5)
                    # cv2.line(image, bottomRight, bottomLeft, (255, 0, 0), 5)
                    # cv2.line(image, bottomLeft, topLeft, (255, 0, 0), 5)
                    cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                    cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                    # cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)
                    if (cX == 0 and cY == 0 and count > 1):
                        centroids[markerID[0]] = prev_centroids[markerID[0]]
                    else:
                        centroids[markerID[0]] = (cX, cY)
                        prev_centroids[markerID[0]] = centroids[markerID[0]]
                for i in markerlist:
                    print(i)
                    global_centroids[i] = centroids[i]
                # global_centroids = centroids
                color = (0, 0, 255)
                if (len(centroids) > 1):
                    forwards = ""
                    sideways = ""
                    if previewName == "Side camera":
                        output = cv2.line(image, global_centroids[markerlist[0]], global_centroids[markerlist[1]], color, 2)
                        # output = cv2.line(image, centroids[2], centroids[4], color, 2)
                        # output = cv2.line(image, centroids[4], centroids[6], color, 2)
                        output = cv2.line(image, global_centroids[markerlist[0]], global_centroids[markerlist[1]], (0, 255, 0), 2)
                    elif previewName == "Back camera":
                        output = cv2.line(image, global_centroids[markerlist[0]], global_centroids[markerlist[1]], color, 2)
                        # output = cv2.line(image, centroids[2], centroids[4], color, 2)
                        # output = cv2.line(image, centroids[2], centroids[6], color, 2)
                        output = cv2.line(image, global_centroids[markerlist[0]], global_centroids[markerlist[1]], (0, 255, 0), 2)
                    # print(global_centroids)

                    try:
                        forwardangle = round(calcAngle([global_centroids[sidemarkers[0]], global_centroids[sidemarkers[1]]]), 2)
                        # print("forward angle={} updated by {} at {}".format(forwardangle, threadname, datetime.now().time()))
                    except:
                        forwardangle = 90

                    if forwardangle < 80:
                        if forwardangle < 50:
                            forwards = "F2"
                        else:
                            forwards = "F1"
                        if previousforwardangle in range(80,100):
                            numberforward += 1
                    elif forwardangle > 100:
                        forwards = "Re"
                        if previousforwardangle in range(80,100):
                            numberbackward += 1

                    previousforwardangle = forwardangle

                    try:
                        sidewaysangle = round(calcAngle([global_centroids[backmarkers[0]], global_centroids[backmarkers[1]]]), 2)
                        # print("sideways angle={} updated by {} at {}".format(sidewaysangle, threadname, datetime.now().time()))
                    except:
                        sidewaysangle = 90

                    if sidewaysangle < 80:
                        right = abs(90-sidewaysangle)
                        if right > maxright:
                            maxright = right
                        if sidewaysangle < 70:
                            sideways = "R2"
                        else:
                            sideways = "R1"
                        if previoussidewaysangle in range(80,100):
                            numberright += 1
                            rightstarttime = time.time()
                    elif sidewaysangle > 100:
                        left = abs(90 - sidewaysangle)
                        if left > maxleft:
                            maxleft = left
                        if sidewaysangle < 110:
                            sideways = "L1"
                        else:
                            sideways = "L2"
                        if previoussidewaysangle in range(80,100):
                            numberleft += 1
                            leftstarttime = time.time()
                    elif previoussidewaysangle < 80:
                        rightendtime = time.time()
                        stayedright = rightendtime - rightstarttime
                        timeright += stayedright
                    elif previoussidewaysangle > 100:
                        leftendtime = time.time()
                        stayedleft = leftendtime - leftstarttime
                        timeleft += stayedleft
                    previoussidewaysangle = sidewaysangle


                    if forwards != "" and sideways != "":
                        direction = "{}-{}".format(forwards, sideways)
                    else:
                        if forwards != "":
                            direction = forwards
                        else:
                            direction = sideways
                    # message = direction+",{},{},{}".format(datetime.now().time(), threadname,count)
                    # message = direction + ",{}".format(datetime.now().time())
                    # print(message)
                    # print("{} has entered here at {} with frame number {}".format(threadname, datetime.now().time(), frame_number))
                    overall_update += 1
                    end = time.time()
                    exectime = end - start
                    print(start,end,exectime)
                    message = direction + ",{}".format(datetime.now().time())
                    rowtowrite = [overall_update, "'"+str(datetime.now().time()), forwardangle, sidewaysangle, direction, threadname, count, frame_number, exectime]
                    print(message)
                    sock.sendto((message).encode(), (UDP_IP, UDP_PORT))
                    with open(filename, 'a') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(rowtowrite)
                    count += 1
                    # cv2.putText(output, str(forwardangle), (0, 230), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255))
                    # x= 960*(int(previewName[-1])-1)
                    # cv2.moveWindow(previewName, x, 0)
                    cv2.imshow(previewName, output)
                    cv2.waitKey(1)
            cv2.imshow(previewName, image)
            cv2.waitKey(1)
    finally:
        # Stop streaming
        pipeline.stop()
    cv2.destroyWindow(previewName)
    lock.release()


def calcAngle(c):
    c1 = c[0]
    c2 = c[1]
    (x1,y1)=(c1[0],c1[1])
    (x2,y2)=(c2[0],c2[1])
    if x2 - x1 == 0:
        angle = 90
    else:
        slope1 = (-y2 + y1) / (x2 - x1)
        angle = math.atan(slope1) * 180 / 3.14
        if x2 > x1:
            angle = 180 + angle
    return angle

# Create two threads as follows
# backcameraid = "108322073108"
# sidecameraid = "108322073120"
# sidemarkers = [4,8]
# backmarkers = [1,2]
lock = threading.Lock()
thread1 = camThread("Back camera", backcameraid, backmarkers)
thread2 = camThread("Side camera", sidecameraid, sidemarkers)
thread1.start()
thread2.start()
thread1.join()
thread2.join()

stats_filename = 'stats.csv'
with open(stats_filename, 'w') as statsfile:
    csvwriter = csv.writer(statsfile)
    csvwriter.writerow(['max left', '{}'.format(maxleft)])
    csvwriter.writerow(['max right', '{}'.format(maxright)])
    csvwriter.writerow(['chocolates', '{}'.format(chocolates)])
    csvwriter.writerow(['number left', '{}'.format(numberleft)])
    csvwriter.writerow(['number right', '{}'.format(numberright)])
    csvwriter.writerow(['time left', '{}'.format(timeleft)])
    csvwriter.writerow(['time right', '{}'.format(timeright)])

stream = open("plotingui.py")
read_file = stream.read()
exec(read_file)

