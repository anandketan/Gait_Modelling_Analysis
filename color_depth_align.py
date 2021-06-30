## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.
import time
import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
colorizer = rs.colorizer()

point = (0,0)

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
time.sleep(1)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
time.sleep(1)
decimation = rs.decimation_filter()
profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
print(depth_scale)

def click(event, x,y, flags, param):
    global point, pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Pressed", x,y)
        point = (x,y)
        print("Depth = ",depth_image[y,x]*depth_scale)

cv2.namedWindow('Depth feed', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback("Depth feed", click)
while True:
    frame = pipeline.wait_for_frames()
    align = rs.align(rs.stream.color)
    aligned_frame = align.process(frame)
    depth_frame = aligned_frame.get_depth_frame()
    #decimated_depth = decimation.process(depth_frame)
    #depth_image = np.asanyarray(decimated_depth.get_data())
    color_frame = aligned_frame.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())
    #print(depth_image.shape)
    depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())
    #print(color_image.shape)
    #images = np.hstack((color_image, depth_colormap)) 
    cv2.imshow('Depth feed', depth_colormap)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

pipeline.stop()
# Create alignment primitive with color as its target stream:

