## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

import pyrealsense2 as rs
import numpy as np
import cv2
import datetime

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
colorizer = rs.colorizer()
profile = pipeline.start(config)
decimation = rs.decimation_filter()
decimation.set_option(rs.option.filter_magnitude, 4)
# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(5):
  pipeline.wait_for_frames()
spatial = rs.spatial_filter()
spatial.set_option(rs.option.filter_magnitude, 5)
spatial.set_option(rs.option.filter_smooth_alpha, 1)
spatial.set_option(rs.option.filter_smooth_delta, 50)
hole_filling = rs.hole_filling_filter()
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('normal_depth.avi', fourcc, 15.0, (640, 480))
norm = np.zeros((848,480))
temp = 0
count = 0
cv2.namedWindow('Depth feed', cv2.WINDOW_AUTOSIZE)
while True:
    frames = pipeline.wait_for_frames()
    align = rs.align(rs.stream.color)
    aligned_frame = align.process(frames)
    depth_frame = aligned_frame.get_depth_frame()
    color_frame = aligned_frame.get_color_frame()
    dist = depth_frame.get_distance(319, 239)
    #print(dist)
    color_image = np.asanyarray(color_frame.get_data())
    filtered_depth = spatial.process(depth_frame)
    #filled_depth = hole_filling.process(filtered_depth)
    depth_image = np.asanyarray(filtered_depth.get_data())
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    if(int(ts)%10 == temp):
      count = count+1
    else:
      fps = count
      count = 0
    temp = int(ts)%10
    print(ts)
    final = cv2.convertScaleAbs(depth_image, alpha=(1000.0/65535.0))
    #print(final.shape)
    grey = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
    colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())
    numpy_horizontal = np.hstack((color_image,grey))
    cv2.putText(numpy_horizontal,"fps={0}".format(fps),(50,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
    cv2.imshow('Depth feed', numpy_horizontal)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

pipeline.stop()