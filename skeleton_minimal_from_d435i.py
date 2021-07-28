## License: ?
## Copyright(c) Cubemos GmBH. All Rights Reserved.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

import cmath
import math
import os
import cv2
import numpy as np
import pyrealsense2 as rs
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice #refer to cubmos documentation for installation
from cubemos.skeletontracking.native_wrapper import Api #refer to cubmos documentation for installation
import socket
import pandas as pd
#import pptk


joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

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
direction = ""
sideways = ""
forwards = ""
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
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
def calculateAngle(x1, y1, z1,x2, y2, z2,x3, y3, z3):                   
    ABx = x1 - x2
    ABy = y1 - y2
    ABz = z1 - z2
    BCx = x3 - x2
    BCy = y3 - y2
    BCz = z3 - z2
    dotProduct = ABx * BCx +ABy * BCy +ABz * BCz
    magnitudeAB = ABx * ABx +ABy * ABy +ABz * ABz
    magnitudeBC = BCx * BCx +BCy * BCy +BCz * BCz
    angle = dotProduct
    if (magnitudeAB == 0 or magnitudeBC == 0):
        angle = 0.0
    else:
        angle = cmath.acos(angle/math.sqrt(magnitudeAB *magnitudeBC))
    angle = (angle * 180) / math.pi
    return(round(abs(angle), 4))
##########################################################################################################################
def render_result(skeletons, color_img, depth_img, intr, confidence_threshold):
    #A = np.array([[0,0,0]])
    global direction
    global sideways
    global forwards
    global prev_angle
    global right_count
    global left_count
    neck = (0,0)
    x_neck,y_neck,z_neck = 0,0,0
    mid_hip = (0,0)
    slope = 90
    forward_angle = 0
    #x_face,y_face,z_face = 0,0,0
    right_hip,left_hip = (0,0),(0,0)
    x_mid_hip,y_mid_hip,z_mid_hip = 0,0,0
    skeleton_color = (0, 140, 255)
    #print(f"#Skeletons in frame : {len(skeletons)}")
    if len(skeletons) == 1:
        for index, skeleton in enumerate(skeletons):
            joint_locations,joint_distances = get_valid_coordinates(skeleton, depth_img, confidence_threshold)
            for joint,coordinate in joint_locations.items():
                #x,y,z = 0,0,0
                if joint == 'Right_ear' or joint == 'Left_ear' or joint == 'Right_eye' or joint == 'Left_eye':
                    continue
                elif(joint == 'Neck'):
                    neck = (coordinate[0],coordinate[1])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    x_neck,y_neck,z_neck = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    #A = np.append(A,[np.array([x_neck,y_neck,z_neck])],axis=0)
                elif(joint == 'Right_knee'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
                elif(joint == 'Left_knee'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
                elif(joint == 'Right_hip'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
                    right_hip = (coordinate[0],coordinate[1])
                elif(joint == 'Left_hip'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
                    left_hip = (coordinate[0],coordinate[1])
                elif(joint == 'Right_shoulder'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
                else:
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
            mid_hip = (math.ceil((left_hip[0]+right_hip[0])/2),math.ceil((left_hip[1]+right_hip[1])/2))
            distance,_,_,_ = cv2.mean((depth_img[mid_hip[1]-3:mid_hip[1]+3,mid_hip[0]-3:mid_hip[0]+3].astype(float))*depth_scale)
            x_mid_hip,y_mid_hip,z_mid_hip = convert_depth_to_phys_coord_using_realsense(intr, neck[0], mid_hip[1], distance)
            if((mid_hip[0]-neck[0])!=0):
                slope = math.atan((mid_hip[1]-neck[1])/(mid_hip[0]-neck[0]))
            else:
                slope = math.pi/2
            slope = (slope * 180) / math.pi
            if(slope<0):
                slope = 180+slope
            forwards = ""
            if(slope>=right_limit and slope<=left_limit):
                sideways = ""
            if slope < right_limit:
                if slope < right_limit_extreme:
                    sideways = "R2"
                else:
                    sideways = "R1"
            elif slope > left_limit:
                if slope < left_limit_extreme:
                    sideways = "L1"
                else:
                    sideways = "L2"
            forward_angle = calculateAngle(x_neck,y_neck,z_neck,x_mid_hip,y_mid_hip,z_mid_hip,x_mid_hip,(y_mid_hip+0.25),z_mid_hip)
            if forward_angle < forward_limit:
                if forward_angle < forward_limit_extreme:
                    forwards = "F2"
                else:
                    forwards = "F1"
            elif forward_angle > 180:
                forwards = "Re"


            if(prev_angle<0 and (90-slope)>0 and slope<right_limit):
                right_count = right_count +1
            elif(prev_angle>0 and (90-slope)<0 and slope>left_limit):
                left_count = left_count + 1

            if(prev_angle == 0 and (90-slope)<0):
                prev_angle = 90-slope
            elif(prev_angle == 0 and (90-slope)>0):
                prev_angle = 90-slope
            elif((90-slope)<0):
                prev_angle = 90-slope
            elif((90-slope)>0):
                prev_angle = 90-slope 
            
            angle_data.append([180-forward_angle,90-slope])
            cv2.putText(color_img,"forward_angle={0:.6}".format(forward_angle),(850,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(color_img,"sway_angle={0:.6}".format(slope),(50,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
            #v.clear()
            #v.load(A)
            #v.set(point_size=0.01)
            if forwards != "" and sideways != "":
                direction = "{}-{}".format(forwards, sideways)
            else:
                if forwards != "":
                    direction = forwards
                else:
                    direction = sideways
            message = direction 
            sock.sendto((message).encode(), (UDP_IP, UDP_PORT))
            #print(message)
            cv2.imshow('Skeleton', color_img)    
            #out.write(color_img)
    else:
        cv2.imshow('Skeleton', color_img)    
        #out.write(color_img)
##########################################################################################################################
#v = pptk.viewer(np.array([[0,0,0]]))




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

df = pd.DataFrame(angle_data,columns=['Forward angle','Sway_angle'])
df.to_csv ('two_angles.csv', index = False, header=True)

print("Max left angle : {0:.4}".format(df.loc[df.Sway_angle > -40.0,'Sway_angle'].min()))
print("Max right angle : {0:.4}".format(df.loc[df.Sway_angle < 40.0,'Sway_angle'].max()))
print(f"left count : {left_count}")
print(f"right count : {right_count}")