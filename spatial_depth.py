import cv2
import numpy as np
import pyrealsense2 as rs
import pandas as pd
import os
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice
from cubemos.skeletontracking.native_wrapper import Api 
import math

joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license")

api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)
colorizer = rs.colorizer()
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 15)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

for x in range(5):
  pipeline.wait_for_frames()

spatial = rs.spatial_filter()


def get_valid_coordinates(skeleton, depth, confidence_threshold):
    result_coordinate = {}
    result_distance = {}
    for i in range (len(skeleton.joints)):
        if skeleton.confidences[i] >= confidence_threshold:
            if skeleton.joints[i][0] >= 0 and skeleton.joints[i][1] >= 0:
                result_coordinate[joints[i]] = tuple(map(int, skeleton.joints[i]))
                dist,_,_,_ = cv2.mean((depth[result_coordinate[joints[i]][1]-3:result_coordinate[joints[i]][1]+3,result_coordinate[joints[i]][0]-3:result_coordinate[joints[i]][0]+3].astype(float))*depth_scale)
                result_distance[joints[i]] = dist
    return result_coordinate,result_distance

def convert_depth_to_phys_coord_using_realsense(intrin,x, y, depth):  
    #print("x={},y={}".format(x,y))
    result = rs.rs2_deproject_pixel_to_point(intrin, [x, y], depth)  
    #result[0]: right (x), result[1]: down (y), result[2]: forward (z) from camera POV
    return result[0], result[1], result[2]

def render_result(skeletons, color_img, depth_img, intr, confidence_threshold,alpha):
    #depth_frame.__class__ = rs.pyrealsense2.depth_frame
    white = np.zeros([640,800,3],dtype=np.uint8)
    white.fill(255)
    skeleton_color = (0, 140, 255)
    #print(f"#Skeletons in frame : {len(skeletons)}")
    final = cv2.convertScaleAbs(depth_img, alpha=(alpha/65535.0))
    grey = cv2.cvtColor(final, cv2.COLOR_GRAY2BGR)
    if len(skeletons) == 1:
        for index, skeleton in enumerate(skeletons):
            joint_locations,joint_distances = get_valid_coordinates(skeleton, depth_img, confidence_threshold)
            for joint,coordinate in joint_locations.items():
                #x,y,z = 0,0,0
                if joint == 'Right_ear' or joint == 'Left_ear' or joint == 'Right_eye' or joint == 'Left_eye':
                    continue
                elif(joint == 'Neck'):
                    cv2.circle(grey, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    x,y,z = convert_depth_to_phys_coord_using_realsense(intr, math.floor(coordinate[0]), math.floor(coordinate[1]), joint_distances[joint])
                    true_dist = math.sqrt((x**2)+(y**2)+(z**2))
                    cv2.putText(white,"xyz = {0:.4},{1:.4},{2:.4}".format(x,y,z),(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
                    cv2.putText(white,"trueDist = {0:.4}".format(true_dist),(20,120), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,154),2,cv2.LINE_AA)
                    cv2.putText(white,"Difference = {0:.5}".format((true_dist-z)),(20,230), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,154),2,cv2.LINE_AA)
                else:
                    cv2.circle(grey, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
            
            
            #print(message)
            numpy_horizontal = np.hstack((color_img,grey))
            cv2.imshow('Skeleton', numpy_horizontal)    
            cv2.imshow('Output',white)
            #out.write(color_img)
    else:
        numpy_horizontal = np.hstack((color_img,grey))
        cv2.imshow('Skeleton', numpy_horizontal)  
        cv2.imshow('Output',white)   
        #out.write(color_img)

cv2.namedWindow('Skeleton', cv2.WINDOW_AUTOSIZE)
cv2.namedWindow('Output', cv2.WINDOW_AUTOSIZE)

def nothing(x):
    os.system('cls||clear')
    
cv2.namedWindow('Controls')
cv2.createTrackbar("Filter Magnitude", "Controls", 1, 5, nothing)
cv2.createTrackbar("Smooth Alpha", "Controls", 25, 100, nothing)
cv2.createTrackbar("Smooth Delta", "Controls", 1, 50, nothing)
cv2.createTrackbar("Alpha", "Controls", 1, 400, nothing)

while True:
    frame = pipeline.wait_for_frames()
    align = rs.align(rs.stream.color)
    aligned_frame = align.process(frame)
    depth_frame = aligned_frame.get_depth_frame()
    color_frame = aligned_frame.get_color_frame()
    mag = cv2.getTrackbarPos("Filter Magnitude", 'Controls')
    alpha = cv2.getTrackbarPos("Smooth Alpha", 'Controls')
    delta = cv2.getTrackbarPos("Smooth Delta", 'Controls')
    newValue1 = cv2.getTrackbarPos("Alpha", 'Controls')*100
    spatial.set_option(rs.option.filter_magnitude, mag)
    spatial.set_option(rs.option.filter_smooth_alpha, (alpha/100))
    spatial.set_option(rs.option.filter_smooth_delta, delta)
    spatial_depth_frame = spatial.process(depth_frame)
    colorized_depth = np.asanyarray(colorizer.colorize(spatial_depth_frame).get_data())
    prof = spatial_depth_frame.get_profile()
    video_prof = prof.as_video_stream_profile()
    intrinsics = video_prof.get_intrinsics()
    print(intrinsics)
    depth_image_spatial = np.asanyarray(spatial_depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    skeletons = api.estimate_keypoints(color_image, 192) 
    render_result(skeletons, colorized_depth,depth_image_spatial, intrinsics, 0.6,newValue1)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindow()
        break
pipeline.stop()