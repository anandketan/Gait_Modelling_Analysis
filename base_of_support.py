import cmath
import math
import os
import cv2
import numpy as np
import pyrealsense2 as rs
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice #refer to cubmos documentation for installation
from cubemos.skeletontracking.native_wrapper import Api #refer to cubmos documentation for installation
#import socket

joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

#UDP_IP = "192.168.100.202" #CIT Lab fancy computer on the right side from the entrance when one faces towards the room 192.168.164.170
#UDP_PORT = 5065
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license") 

api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()
colorizer = rs.colorizer()

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

def calculateDistance(x1, y1, z1,x2, y2, z2): 
    return(math.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2))

def calculate2dAngle(x1,y1,x2,y2):
    if((x2-x1)!=0):
        return((math.atan(y2-y1)/(x2-x1))*180/math.pi)
    else:
        return((math.pi/2)*180/math.pi)

def calculate3dAngle(x1, y1, z1,x2, y2, z2,x3, y3, z3):                   
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

def render_result(skeletons, color_img, depth_img, intr, confidence_threshold):
    white = np.zeros([512,512,3],dtype=np.uint8)
    white.fill(255)
    #A = np.array([[0,0,0]])
    right_knee = [0,0,0]
    left_knee = [0,0,0]
    right_ankle = [0,0,0]
    left_ankle = [0,0,0]
    rk = [0,0]
    lk = [0,0]
    la = [0,0]
    ra = [0,0]
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
                    #A = np.append(A,[np.array([x_neck,y_neck,z_neck])],axis=0)
                elif(joint == 'Right_knee'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    right_knee[0],right_knee[1],right_knee[2] = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    rk = coordinate
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
                elif(joint == 'Left_knee'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    left_knee[0],left_knee[1],left_knee[2] = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    lk = coordinate
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
                elif(joint == 'Left_ankle'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    left_ankle[0],left_ankle[1],left_ankle[2] = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    la = coordinate
                elif(joint == 'Right_ankle'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    right_ankle[0],right_ankle[1],right_ankle[2] = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    ra = coordinate
                else:
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    #x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    #A = np.append(A,[np.array([x,y,z])],axis=0)
            knee_dist = calculateDistance(right_knee[0],right_knee[1],right_knee[2],left_knee[0],left_knee[1],left_knee[2])
            foot_dist = calculateDistance(right_ankle[0],right_ankle[1],right_ankle[2],left_ankle[0],left_ankle[1],left_ankle[2])
            print(abs(right_ankle[1]-left_ankle[1]))
            if(abs(right_ankle[1]-left_ankle[1])<0.7):
                if((right_ankle[0]>0 and left_ankle[0]>0) or (right_ankle[0]<0 and left_ankle[0]<0)):
                    area = abs(right_ankle[2]-left_ankle[2])*abs(right_ankle[0]-left_ankle[0])
                else:
                    area = abs(right_ankle[2]-left_ankle[2])*(abs(right_ankle[0])+abs(left_ankle[0]))
                #if(area == 0):

            else:
                area = 100.0
            
            #cv2.putText(white,"foot_distance = {0:.4}".format(foot_dist),(20,20), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2,cv2.LINE_AA)
            #cv2.putText(white,"knee_distance = {0:.4}".format(knee_dist),(20,120), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
            cv2.putText(white,"knee_distance = {0}".format(area),(20,220), cv2.FONT_HERSHEY_SIMPLEX, 1,(186,255,0),2,cv2.LINE_AA)
            cv2.putText(white,"Right_ankle = {0:.3},{1:.3},{2:.3}".format(right_ankle[0],right_ankle[1],right_ankle[2]),(20,20), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
            cv2.putText(white,"Left_ankle = {0:.3},{1:.3},{2:.3}".format(left_ankle[0],left_ankle[1],left_ankle[2]),(20,120), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
            #sock.sendto((message).encode(), (UDP_IP, UDP_PORT))
            cv2.imshow('Skeleton', color_img)  
            cv2.imshow('Output',white)  
            #out.write(color_img)
    else:
        cv2.imshow('Skeleton', color_img) 
        cv2.imshow('Output',white)   
        #out.write(color_img)

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
    skeletons = api.estimate_keypoints(color_image, 192) #256,288,314,320
    render_result(skeletons, color_image, depth_image, intrinsics, 0.45)
    cv2.namedWindow('Skeleton', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('Output', cv2.WINDOW_AUTOSIZE)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyWindow('Skeleton')
        cv2.destroyWindow('Output')
        break
pipeline.stop()