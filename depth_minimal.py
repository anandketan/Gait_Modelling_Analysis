## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
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

while True:
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    dist = depth_frame.get_distance(319, 239)
    print(dist)
    depth_image = np.asanyarray(depth_frame.get_data())
    #print(depth_image.shape)
    prof = depth_frame.get_profile()
    video_prof = prof.as_video_stream_profile()
    intrinsics = video_prof.get_intrinsics()
    #print(type(intrinsics))
    filtered_depth = spatial.process(depth_frame)
    #filled_depth = hole_filling.process(filtered_depth)
    colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())
    #print(colorized_depth.shape)
    #decimated_depth = decimation.process(depth_frame)
    #depth_colormap = np.asanyarray(colorizer.colorize(decimated_depth).get_data()) 
    #depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data()) 
 #   out.write(depth_colormap)
    cv2.namedWindow('Depth feed', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('Depth feed', colorized_depth)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

pipeline.stop()