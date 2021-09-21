from tifffile import imsave
import pyrealsense2 as rs
import numpy as np
import cv2
import os
import datetime
from PIL import Image 

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
colorizer = rs.colorizer()
decimation = rs.decimation_filter()
decimation.set_option(rs.option.filter_magnitude, 4)
profile = pipeline.start(config)
for x in range(5):
  pipeline.wait_for_frames()

def nothing(x):
  os.system('cls||clear')



cv2.namedWindow('Controls')
cv2.createTrackbar("Alpha", "Controls", 1, 400, nothing)
#cv2.createTrackbar("Filter Size", "Controls", 0, 7, nothing)

norm = np.zeros((480,848,1))
print(norm.shape)

k=0
temp=0
count=0
fps = 0
while True:
  k = k+1
  frame = pipeline.wait_for_frames()
  align = rs.align(rs.stream.color)
  aligned_frames = align.process(frame)
  depth_frame = aligned_frames.get_depth_frame()
  decimated_depth_frame = decimation.process(depth_frame)
  depth_image_decimated = np.asanyarray(decimated_depth_frame.get_data())
  aligned_color_frame = aligned_frames.get_color_frame()
  color_image_decimated = np.asanyarray(aligned_color_frame.get_data())
  print(color_image_decimated.shape)
  alp = cv2.getTrackbarPos("Alpha", 'Controls')*100
  #filter_size = cv2.getTrackbarPos("Filter Size", 'Controls') + 1
  ct = datetime.datetime.now()
  ts = ct.timestamp()
  if(int(ts)%10 == temp):
    count = count+1
  else:
    fps = count
    count = 0
  temp = int(ts)%10
  Image.fromarray(depth_image_decimated).save(f"/home/kathir/Desktop/tiff_images/test-{k}.tiff")  
  #print(depth_image.shape)
  final = cv2.convertScaleAbs(depth_image_decimated, alpha=(alp/65535.0))
  #norm = np.dstack((norm,depth_image))
  grey = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
  #print(grey.shape)
  cv2.putText(grey,"fps={0}".format(fps),(50,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
  cv2.imshow('Depth feed', grey)
  key = cv2.waitKey(1)
  # Press esc or 'q' to close the image window
  if key & 0xFF == ord('q') or key == 27:
      cv2.destroyAllWindows()
      break
print(norm.shape)
pipeline.stop()