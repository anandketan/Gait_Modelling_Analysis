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


joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']
def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license") #"LOCALAPPDATA" in place of "HOME" for windows 10


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter('skeleton_coordinates.mp4', 0x7634706d, 15.0, (1280, 720))

api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

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
    result = rs.rs2_deproject_pixel_to_point(intrin, [x, y], depth)  
    #result[0]: right (x), result[1]: down (y), result[2]: forward (z) from camera POV
    return result[0], result[1], result[2]

def calculateAngle(x1, y1, z1,
                   x2, y2, z2,
                   x3, y3, z3):
                        
    # Find direction ratio of line AB
    ABx = x1 - x2
    ABy = y1 - y2
    ABz = z1 - z2
 
    # Find direction ratio of line BC
    BCx = x3 - x2
    BCy = y3 - y2
    BCz = z3 - z2
 
    # Find the dotProduct of lines AB & BC
    dotProduct = (ABx * BCx +ABy * BCy +ABz * BCz)
 
    # Find magnitude of line AB and BC
    magnitudeAB = ABx * ABx +ABy * ABy +ABz * ABz
    magnitudeBC = BCx * BCx +BCy * BCy +BCz * BCz
 
    # Find the cosine of the angle formed by line AB and BC
    angle = dotProduct
    if (magnitudeAB == 0 or magnitudeBC == 0):
        angle = 0.0
    else:
        angle = cmath.acos(angle/math.sqrt(magnitudeAB *magnitudeBC))
 
    # Find angle in radian
    angle = (angle * 180) / math.pi
 
    # Print angle
    return(round(abs(angle), 4))

def render_result(skeletons, color_img, depth_img, intr, confidence_threshold):
    x_rw,y_rw,z_rw,x_re,y_re,z_re,x_rs,y_rs,z_rs,x_lw,y_lw,z_lw,x_le,y_le,z_le,x_ls,y_ls,z_ls = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    #x_face,y_face,z_face = 0,0,0
    skeleton_color = (100, 254, 213)
    if len(skeletons) == 1:
        #A = np.array([[0,0,0]])
        for index, skeleton in enumerate(skeletons):
            joint_locations,joint_distances = get_valid_coordinates(skeleton, depth_img, confidence_threshold)
            #print ("Resultant dictionary is : " +  str(joint_locations))
            for joint,coordinate in joint_locations.items():
                """
                if(joint == 'Nose'):
                    x_face,y_face,z_face = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    cv2.putText(color_img,"x={0:.3} y={1:.3} z={2:.3} depth = {3:.3}".format(x_face,y_face,z_face,joint_distances[joint]),coordinate, cv2.FONT_HERSHEY_SIMPLEX, 0.5,(165,44,59),2,cv2.LINE_AA)
                """
                if joint == 'Right_ear' or joint == 'Left_ear' or joint == 'Right_eye' or joint == 'Left_eye':
                    continue
                elif(joint == 'Right_wrist'):
                    x_rw,y_rw,z_rw = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #print("x_rw = {0} y_rw = {1} z_rw = {2}".format(x_rw,y_rw,z_rw))
                elif(joint == 'Right_elbow'):
                    x_re,y_re,z_re = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #print("x_re = {0} y_re = {1} z_re = {2}".format(x_re,y_re,z_re))
                elif(joint == 'Right_shoulder'):
                    x_rs,y_rs,z_rs = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #print("x_rs = {0} y_rs = {1} z_rs = {2}".format(x_rs,y_rs,z_rs))
                elif(joint == 'Left_wrist'):
                    x_lw,y_lw,z_lw = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #print("x_lw = {0} y_lw = {1} z_lw = {2}".format(x_lw,y_lw,z_lw))
                elif(joint == 'Left_elbow'):
                    x_le,y_le,z_le = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #print("x_le = {0} y_le = {1} z_le = {2}".format(x_le,y_le,z_le))
                elif(joint == 'Left_shoulder'):
                    x_ls,y_ls,z_ls = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #print("x_ls = {0} y_ls = {1} z_ls = {2}".format(x_ls,y_ls,z_ls))
                else:
                    x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #cv2.putText(color_img,"x={0} y={1} z={2}".format(x,y,z),coordinate, cv2.FONT_HERSHEY_SIMPLEX, 0.5,(165,44,59),2,cv2.LINE_AA)
                
            right_angle = calculateAngle(x_rw,y_rw,z_rw,x_re,y_re,z_re,x_rs,y_rs,z_rs)
            cv2.putText(color_img,"right_angle={0}".format(right_angle),(50,25), cv2.FONT_HERSHEY_SIMPLEX, 1,(165,144,59),2,cv2.LINE_AA)
            left_angle = calculateAngle(x_lw,y_lw,z_lw,x_le,y_le,z_le,x_ls,y_ls,z_ls)
            cv2.putText(color_img,"left_angle={0}".format(left_angle),(100,350), cv2.FONT_HERSHEY_SIMPLEX, 1,(165,144,59),2,cv2.LINE_AA)
            #flipped = cv2.flip(color_img, 1)
            cv2.imshow('Skeleton', color_img)    
            out.write(color_img)
    else:
        cv2.imshow('Skeleton', color_img)    
        out.write(color_img)


while True:
    frame = pipeline.wait_for_frames()
    align = rs.align(rs.stream.color)
    aligned_frame = align.process(frame)
    depth_frame = aligned_frame.get_depth_frame()
    prof = depth_frame.get_profile()
    video_prof = prof.as_video_stream_profile()
    intrinsics = video_prof.get_intrinsics()
    depth_image = np.asanyarray(depth_frame.get_data())
    color_frame = aligned_frame.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    #depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())
    skeletons = api.estimate_keypoints(color_image, 256) 
    cv2.namedWindow('Skeleton', cv2.WINDOW_AUTOSIZE)
    render_result(skeletons, color_image, depth_image, intrinsics, 0.6)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break
pipeline.stop()
