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
# import socket
import pandas as pd
# import pptk
import open3d as o3d




joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear', 'Camera']

lines = [[0,14], [0,15], [14,16], [15,17], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [2,8], [8,9], [9,10], [5,11], [11,12], [12,13]]
#random coordinates from a previous experiment. Setting everything to zero doesn't seem to work
coords3d=  {'Nose': (0.20487046241760254, -0.10028954595327377, 1.2699167728424072),
'Neck': (0.19302140176296234, 0.04428612068295479, 1.3540000915527344),
'Right_shoulder': (0.03314350172877312, 0.03538845479488373, 1.3572778701782227),
'Right_elbow': (-0.04068613797426224, 0.24781912565231323, 1.3216111660003662),
'Right_wrist': (-0.08127983659505844, 0.29209014773368835, 1.0844722986221313),
'Left_shoulder': (0.34972065687179565, 0.04387727379798889, 1.3415000438690186),
'Left_elbow': (0.44440022110939026, 0.25280147790908813, 1.3021111488342285),
'Left_wrist': (0.4161774814128876, 0.2813136875629425, 1.0985833406448364),
'Right_hip': (0,0,0),
'Right_knee': (0,0,0),
'Right_ankle': (0,0,0),
'Left_hip': (0,0,0),
'Left_knee': (0,0,0),
'Left_ankle': (0,0,0),
'Right_eye': (0.17547458410263062, -0.14218689501285553, 1.280500054359436),
'Left_eye': (0.22900129854679108, -0.13275755941867828, 1.2715556621551514),
'Right_ear': (0.12736432254314423, -0.143180713057518, 1.3713889122009277),
'Left_ear': (0.28060203790664673, -0.13001656532287598, 1.329805612564087),
'Camera': (0,0,0)}

#for the workaround for undetected joints
prev_joint_3d_coords ={key: (0,0,0) for key in joints}

df = pd.DataFrame.from_dict(coords3d, orient="index", columns=["X", "Y", "Z"])
x = df.to_numpy()

# x= np.zeros((19,3)) # doesn't work for some reason

points = x

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)

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
    return result[0], -result[1], -result[2]
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
########################################################################################################################
def update_visualization(joint_3d_coords):
    df = pd.DataFrame.from_dict(joint_3d_coords, orient="index", columns=["X", "Y", "Z"])
    x = df.to_numpy()
    print("coords3d= ",x)
    points = x
    line_set.points = o3d.utility.Vector3dVector(points)
    pcd.points = o3d.utility.Vector3dVector(points)
    vis.update_geometry(line_set)
    vis.update_geometry(pcd)
    vis.update_renderer()
    vis.poll_events()
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
            # print("joint locations:", joint_locations)
            # print("joint distances:", joint_distances)
            for joint,coordinate in joint_locations.items():
                cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                joint_3d_coords[joint] = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
            # print("coords3d= ",joint_3d_coords)
            # This loop sets an undetected joint's coordinates to its previous detected value. This is the simplest way to deal with undetected joints(not the greatest of course)  
            for joint, coordinate in joint_3d_coords.items():
                if coordinate == (0,0,0):
                    joint_3d_coords[joint] = prev_joint_3d_coords[joint]
                else:
                    prev_joint_3d_coords[joint] = joint_3d_coords[joint]
            update_visualization(joint_3d_coords)
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

#plotting inital set of points. Can't figure out how to get the right view otherwise 
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
colors = [[1, 0, 0] for i in range(len(lines))]
line_set = o3d.geometry.LineSet()
line_set.points = o3d.utility.Vector3dVector(points)
line_set.lines = o3d.utility.Vector2iVector(lines)
line_set.colors = o3d.utility.Vector3dVector(colors)
vis = o3d.visualization.Visualizer()
vis.create_window(width=640, height=360)
vis.add_geometry(line_set)
vis.add_geometry(pcd)

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