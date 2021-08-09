## License: ?
## Copyright(c) Cubemos GmBH. All Rights Reserved.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

# Run this file initially to get the initial position of the player
# Positions(2d, 3d) are stored in pickle files which need to be imported in the main code to get initial positions/angles
# Use for calibration

import cmath
import math
import os
import cv2
import numpy as np
import pyrealsense2 as rs
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice #refer to cubmos documentation for installation
from cubemos.skeletontracking.native_wrapper import Api #refer to cubmos documentation for installation
import pandas as pd
from datetime import datetime
import pickle
import math


joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

prev_joint_3d_coords ={key: (0,0,0) for key in joints}
prev_joint_locations = {key: (0,0) for key in joints}
prev_joint_distances = {key: 0 for key in joints}

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)

distance_data2d = []
position_data2d = []
position_data3d = []

#To save video
#out = cv2.VideoWriter('skeleton_coordinates.mp4', 0x7634706d, 15.0, (1280, 720))
##########################################################################################################################
def default_license_dir():
     return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license") #"LOCALAPPDATA" in place of "HOME" for windows 10
    #return os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "license")
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
def get_initial_position():
    # print("3d pos:", position_data3d)
    # print("2d pos:", position_data2d)
    # print("2d dis:", distance_data2d)
    df = pd.DataFrame(position_data3d ,columns=joints)
    df2 = pd.DataFrame(position_data2d ,columns=joints)
    df3 = pd.DataFrame(distance_data2d ,columns=joints)
    old_cols = df.columns
    for i in old_cols:
        df[['{}X'.format(i), '{}Y'.format(i), '{}Z'.format(i)]] = pd.DataFrame(df[i].tolist(), index=df.index)
        df2[['{}X'.format(i), '{}Y'.format(i)]] = pd.DataFrame(df2[i].tolist(), index=df.index)
    df.drop(columns=old_cols, inplace=True)
    df2.drop(columns=old_cols, inplace=True)
    df.replace(0, np.nan, inplace=True)
    df2.replace(0, np.nan, inplace=True)
    df3.replace(0, np.nan, inplace=True)
    df.to_csv("reachstepout_position3d.csv")
    df2.to_csv("reachstepout_position2d.csv")
    df3.to_csv("reachstepout_distance2d.csv")
    init_pos3d = {key: (0,0,0) for key in joints}
    init_pos3d_median = {key: (0,0,0) for key in joints}
    init_pos2d = {key: (0,0) for key in joints}
    init_pos2d_median = {key: (0,0) for key in joints}
    init_dis2d = {key: 0 for key in joints}
    init_dis2d_median = {key: 0 for key in joints}
    for i in joints:
        try:
            init_pos3d[i] = (df['{}X'.format(i)].mean(), df['{}Y'.format(i)].mean(), df['{}Z'.format(i)].mean())
            init_pos3d_median[i] = (df['{}X'.format(i)].median(), df['{}Y'.format(i)].median(), df['{}Z'.format(i)].median())
        except:
            init_pos3d[i] = (0,0,0)
            init_pos3d_median[i] = (0,0,0)
        try:
            init_pos2d[i] = (round(df2['{}X'.format(i)].mean()), round(df2['{}Y'.format(i)].mean()))
            init_pos2d_median[i] = (round(df2['{}X'.format(i)].median()), round(df2['{}Y'.format(i)].median()))
        except:
            init_pos2d[i] = (0,0)
            init_pos2d_median[i] = (0,0)
        try:
            init_dis2d[i] = df3[i].mean()
            init_dis2d_median[i] = df3[i].median()
        except:
            init_dis2d[i] = 0
            init_dis2d_median[i] = 0
    return [init_pos3d, init_pos3d_median, init_pos2d, init_pos2d_median, init_dis2d, init_dis2d_median]
##########################################################################################################################
def render_result(skeletons, color_img, depth_img, intr, confidence_threshold):
    neck = (0,0)
    x_neck,y_neck,z_neck = 0,0,0
    mid_hip = (0,0)
    #x_face,y_face,z_face = 0,0,0
    right_hip,left_hip = (0,0),(0,0)
    x_mid_hip,y_mid_hip,z_mid_hip = 0,0,0
    skeleton_color = (0, 140, 255)
    #print(f"#Skeletons in frame : {len(skeletons)}")
    if len(skeletons) == 1:
        for index, skeleton in enumerate(skeletons):
            joint_locations,joint_distances = get_valid_coordinates(skeleton, depth_img, confidence_threshold)
            # print(joint_locations.keys)
            joint_3d_coords = {key: (0,0,0) for key in joints}
            joint_2d_coords = {key: (0,0) for key in joints}
            joint_2d_distances = {key: 0 for key in joints}
            # print("joint locations:", joint_locations)
            # print("joint distances:", joint_distances)
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
            # print("Joint locations", joint_locations)
            # print("Joint 2d coords", joint_2d_coords)
            # print("coords3d= ",joint_3d_coords)
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
            cv2.circle(color_img, mid_hip, radius=5, color=(0,0,255), thickness=-1)
            distance,_,_,_ = cv2.mean((depth_img[mid_hip[1]-3:mid_hip[1]+3,mid_hip[0]-3:mid_hip[0]+3].astype(float))*depth_scale)
            x_mid_hip,y_mid_hip,z_mid_hip = convert_depth_to_phys_coord_using_realsense(intr, neck[0], mid_hip[1], distance)
            if((mid_hip[0]-neck[0])!=0):
                slope = math.atan((mid_hip[1]-neck[1])/(mid_hip[0]-neck[0]))
            else:
                slope = math.pi/2
            slope = (slope * 180) / math.pi
            if(slope<0):
                slope = 180+slope
            forward_angle = calculateAngle(x_neck,y_neck,z_neck,x_mid_hip,y_mid_hip,z_mid_hip,x_mid_hip,(y_mid_hip+0.25),z_mid_hip)
            cv2.putText(color_img,"forward_angle={0:.6}".format(forward_angle),(850,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
            cv2.putText(color_img,"sway_angle={0:.6}".format(slope),(50,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
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
initial = [initial3d_by_mean, initial3d_by_median, initial2d_by_mean, initial2d_by_median, initial2d_dis_by_mean, initial2d_dis_by_median] = get_initial_position()
# print("Pos 3d By Mean:", initial3d_by_mean)
# print("Pos 3d By Median:", initial3d_by_median)
# print("Pos 2d By Mean:", initial2d_by_mean)
# print("Pos 2d By Median:", initial2d_by_median)
# print("Dis 2d By Mean:", initial2d_dis_by_mean)
# print("Dis 2d By Median:", initial2d_dis_by_median)
for i,j in zip(initial,['initial3d_by_mean', 'initial3d_by_median', 'initial2d_by_mean', 'initial2d_by_median', 'initial2d_dis_by_mean', 'initial2d_dis_by_median']):
    with open("{}.pkl".format(j), "wb") as file:
        pickle.dump(i,file)
