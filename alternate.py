## License: ?
## Copyright(c) Cubemos GmBH. All Rights Reserved.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

import cmath
import math
import os
from utils import calculateAngle3d, calculateAngleFromSlope, direction_string_generator, forwards_string_generator, is_reach_out_left, is_reach_out_right, save_positional_to_csv, sway_string_generator
import cv2
import numpy as np
import pyrealsense2 as rs
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice #refer to cubmos documentation for installation
from cubemos.skeletontracking.native_wrapper import Api #refer to cubmos documentation for installation
import socket
import pandas as pd

joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

prev_joint_3d_coords ={key: (0,0,0) for key in joints}
prev_joint_locations = {key: (0,0) for key in joints}
prev_joint_distances = {key: 0 for key in joints}

distance_data2d = []
position_data2d = []
position_data3d = []

UDP_IP = "192.168.100.202" #CIT Lab fancy computer on the right side from the entrance when one faces towards the room 192.168.164.170
UDP_PORT = 5065
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

prev_angle = 0.0
right_count = 0
left_count = 0
time_on_left = 0
time_on_right = 0
angle_data = [[0,0]]
right_limit = 85
right_limit_extreme = 80
left_limit = 95
left_limit_extreme = 100
forward_limit = 170
forward_limit_extreme = 165
reverse_limit = 185
direction = ""
sideways = ""
forwards = ""
reachout_right = False
reachout_left = False
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 15)
#config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)

#To save video
#out = cv2.VideoWriter('skeleton_coordinates.mp4', 0x7634706d, 15.0, (1280, 720))
##########################################################################################################################
def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license") #"LOCALAPPDATA" in place of "HOME" for windows 10
##########################################################################################################################
api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
colorizer = rs.colorizer()
##########################################################################################################################
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
##########################################################################################################################
def convert_depth_to_phys_coord_using_realsense(intrin,x, y, depth):  
    result = rs.rs2_deproject_pixel_to_point(intrin, [x, y], depth)  
    #result[0]: right (x), result[1]: down (y), result[2]: forward (z) from camera POV
    return result[0], result[1], result[2]
##########################################################################################################################
def render_result(skeletons, color_img, depth_img, intr, confidence_threshold):
    global direction
    global sideways
    global forwards
    global prev_angle
    global right_count
    global left_count
    neck = (0,0)
    x_neck,y_neck,z_neck = 0,0,0
    mid_hip = (0,0)
    sway_angle = 90
    forward_angle = 0
    right_hip,left_hip = (0,0),(0,0)
    x_mid_hip,y_mid_hip,z_mid_hip = 0,0,0
    skeleton_color = (0, 140, 255)
    if len(skeletons) == 1:
        for index, skeleton in enumerate(skeletons):
            joint_locations,joint_distances = get_valid_coordinates(skeleton, depth_img, confidence_threshold)
            joint_3d_coords = {key: (0,0,0) for key in joints}
            joint_2d_coords = {key: (0,0) for key in joints}
            joint_2d_distances = {key: 0 for key in joints}
            for joint,coordinate in joint_locations.items():
                cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                joint_3d_coords[joint] = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                joint_2d_coords[joint] = joint_locations[joint]
                joint_2d_distances[joint] = joint_distances[joint]
            for joint, coordinate in joint_3d_coords.items():
                if coordinate == (0,0,0):
                    joint_2d_coords[joint] = prev_joint_locations[joint]
                    joint_2d_distances[joint] = prev_joint_distances[joint] 
                    joint_3d_coords[joint] = prev_joint_3d_coords[joint]
                else:
                    prev_joint_locations[joint] = joint_2d_coords[joint]
                    prev_joint_distances[joint] = joint_2d_distances[joint]
                    prev_joint_3d_coords[joint] = joint_3d_coords[joint]
            rowtowrite = [j for i,j in joint_3d_coords.items()]
            rowtowrite2 = [j for i,j in joint_2d_coords.items()]
            rowtowrite3 = [j for i,j in joint_2d_distances.items()]
            position_data3d.append(rowtowrite)
            position_data2d.append(rowtowrite2)
            distance_data2d.append(rowtowrite3)
            if 'Neck' in joint_locations:
                neck = joint_locations['Neck']
                (x_neck, y_neck, z_neck) = joint_3d_coords['Neck']
            if 'Left_hip' in joint_locations:
                left_hip = joint_locations['Left_hip']
            if 'Right_hip' in joint_locations:
                right_hip = joint_locations['Right_hip'] 
            mid_hip = (math.ceil((left_hip[0]+right_hip[0])/2),math.ceil((left_hip[1]+right_hip[1])/2))
            distance,_,_,_ = cv2.mean((depth_img[mid_hip[1]-3:mid_hip[1]+3,mid_hip[0]-3:mid_hip[0]+3].astype(float))*depth_scale)
            mid_hip3d = x_mid_hip,y_mid_hip,z_mid_hip = convert_depth_to_phys_coord_using_realsense(intr, neck[0], mid_hip[1], distance)
            sway_angle = calculateAngleFromSlope(neck, mid_hip)
            forwards = ""
            sideways = sway_string_generator(sway_angle, right_limit, left_limit, right_limit_extreme, left_limit_extreme)
            forward_angle = calculateAngle3d(joint_3d_coords['Neck'], mid_hip3d, (x_mid_hip,(y_mid_hip+0.25),z_mid_hip))
            forwards = forwards_string_generator(forward_angle, forward_limit, forward_limit_extreme, reverse_limit)

            reachout_right = is_reach_out_right(joint_2d_coords)
            reachout_left = is_reach_out_left(joint_2d_coords)

            if(prev_angle<0 and (90-sway_angle)>0 and sway_angle<right_limit):
                right_count = right_count +1
            elif(prev_angle>0 and (90-sway_angle)<0 and sway_angle>left_limit):
                left_count = left_count + 1

            if(prev_angle == 0 and (90-sway_angle)<0):
                prev_angle = 90-sway_angle
            elif(prev_angle == 0 and (90-sway_angle)>0):
                prev_angle = 90-sway_angle
            elif((90-sway_angle)<0):
                prev_angle = 90-sway_angle
            elif((90-sway_angle)>0):
                prev_angle = 90-sway_angle 
            
            angle_data.append([180-forward_angle,90-sway_angle])
            cv2.putText(color_img,"forward_angle={0:.6}".format(forward_angle),(850,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(color_img,"sway_angle={0:.6}".format(sway_angle),(50,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
            if reachout_right:
                cv2.putText(color_img,"Reach Out(Right)",(50,250), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
            if reachout_left:
                cv2.putText(color_img,"Reach Out(Left)",(850,250), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
            direction = direction_string_generator(forwards, sideways)
            message = direction 
            sock.sendto((message).encode(), (UDP_IP, UDP_PORT))
            #print(message)
            cv2.imshow('Skeleton', color_img)
    else:
        cv2.imshow('Skeleton', color_img)
##########################################################################################################################

while True:
    frame = pipeline.wait_for_frames()
    align = rs.align(rs.stream.color)
    aligned_frame = align.process(frame)
    depth_frame = aligned_frame.get_depth_frame()
    color_frame = aligned_frame.get_color_frame()
    prof = depth_frame.get_profile()
    video_prof = prof.as_video_stream_profile()
    intrinsics = video_prof.get_intrinsics()
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    #color_imgmap = np.asanyarray(colorizer.colorize(depth_frame).get_data())
    skeletons = api.estimate_keypoints(color_image, 256) 
    render_result(skeletons, color_image, depth_image, intrinsics, 0.6)
    cv2.namedWindow('Skeleton', cv2.WINDOW_AUTOSIZE)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyWindow('Skeleton')
        break
pipeline.stop()

save_positional_to_csv(position_data3d, "coordinates3d", position_data2d, "coordinates2d", distance_data2d, "distances2d")

df = pd.DataFrame(angle_data,columns=['Forward angle','Sway_angle'])
df.to_csv ('two_angles.csv', index = False, header=True)

print("Max left angle : {0:.4}".format(df.loc[df.Sway_angle > -40.0,'Sway_angle'].min()))
print("Max right angle : {0:.4}".format(df.loc[df.Sway_angle < 40.0,'Sway_angle'].max()))
print(f"left count : {left_count}")
print(f"right count : {right_count}")