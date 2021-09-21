## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

import pyrealsense2 as rs
import numpy as np
import cv2
import datetime

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)

point = (0,0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('foot6.avi', fourcc, 30.0, (848, 480))

def click(event, x,y, flags, param):
    global point, pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Pressed", x,y)
        point = (x,y)
        print("BGR = ",color_image[y,x])

cv2.namedWindow('BGR feed', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback("BGR feed", click)
temp = 0
count = 0
fps = 0
while True:
    frames = pipeline.wait_for_frames()
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    if(int(ts)%10 == temp):
      count = count+1
    else:
      fps = count
      count = 0
    temp = int(ts)%10
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    out.write(color_image)
    #cv2.namedWindow('BGR feed', cv2.WINDOW_AUTOSIZE)
    #print(color_image.shape)
    cv2.putText(color_image,"fps={0}".format(fps),(50,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
    cv2.imshow('BGR feed', color_image)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

pipeline.stop()