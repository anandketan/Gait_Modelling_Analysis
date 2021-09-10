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

count = 0

api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

for x in range(5):
  pipeline.wait_for_frames()

spatial = rs.spatial_filter()
spatial.set_option(rs.option.filter_magnitude, 5)
spatial.set_option(rs.option.filter_smooth_alpha, 1)
spatial.set_option(rs.option.filter_smooth_delta, 50)
hole_filling = rs.hole_filling_filter()

decimation = rs.decimation_filter()
decimation.set_option(rs.option.filter_magnitude, 3)
global df
df = pd.DataFrame(columns = ['Nose:X','Nose:Y','Nose:Z','Nose:TrueDistance',
                            'Neck:X','Neck:Y','Neck:Z','Neck:TrueDistance',
                            'Right_shoulder:X','Right_shoulder:Y','Right_shoulder:Z','Right_shoulder:TrueDistance',
                            'Right_elbow:X','Right_elbow:Y','Right_elbow:Z','Right_elbow:TrueDistance',
                            'Right_wrist:X','Right_wrist:Y','Right_wrist:Z','Right_wrist:TrueDistance',
                            'Left_shoulder:X','Left_shoulder:Y','Left_shoulder:Z','Left_shoulder:TrueDistance',
                            'Left_elbow:X','Left_elbow:Y','Left_elbow:Z','Left_elbow:TrueDistance',
                            'Left_wrist:X','Left_wrist:Y','Left_wrist:Z','Left_wrist:TrueDistance',
                            'Right_hip:X','Right_hip:Y','Right_hip:Z','Right_hip:TrueDistance',
                            'Right_knee:X','Right_knee:Y','Right_knee:Z','Right_knee:TrueDistance',
                            'Right_ankle:X','Right_ankle:Y','Right_ankle:Z','Right_ankle:TrueDistance',
                            'Left_hip:X','Left_hip:Y','Left_hip:Z','Left_hip:TrueDistance',
                            'Left_knee:X','Left_knee:Y','Left_knee:Z','Left_knee:TrueDistance',
                            'Left_ankle:X','Left_ankle:Y','Left_ankle:Z','Left_ankle:TrueDistance'])

df = df.append({'Nose:X':0,'Nose:Y':0,'Nose:Z':0,'Nose:TrueDistance':0,
                'Neck:X':0,'Neck:Y':0,'Neck:Z':0,'Neck:TrueDistance':0,
                'Right_shoulder:X':0,'Right_shoulder:Y':0,'Right_shoulder:Z':0,'Right_shoulder:TrueDistance':0,
                'Right_elbow:X':0,'Right_elbow:Y':0,'Right_elbow:Z':0,'Right_elbow:TrueDistance':0,
                'Right_wrist:X':0,'Right_wrist:Y':0,'Right_wrist:Z':0,'Right_wrist:TrueDistance':0,
                'Left_shoulder:X':0,'Left_shoulder:Y':0,'Left_shoulder:Z':0,'Left_shoulder:TrueDistance':0,
                'Left_elbow:X':0,'Left_elbow:Y':0,'Left_elbow:Z':0,'Left_elbow:TrueDistance':0,
                'Left_wrist:X':0,'Left_wrist:Y':0,'Left_wrist:Z':0,'Left_wrist:TrueDistance':0,
                'Right_hip:X':0,'Right_hip:Y':0,'Right_hip:Z':0,'Right_hip:TrueDistance':0,
                'Right_knee:X':0,'Right_knee:Y':0,'Right_knee:Z':0,'Right_knee:TrueDistance':0,
                'Right_ankle:X':0,'Right_ankle:Y':0,'Right_ankle:Z':0,'Right_ankle:TrueDistance':0,
                'Left_hip:X':0,'Left_hip:Y':0,'Left_hip:Z':0,'Left_hip:TrueDistance':0,
                'Left_knee:X':0,'Left_knee:Y':0,'Left_knee:Z':0,'Left_knee:TrueDistance':0,
                'Left_ankle:X':0,'Left_ankle:Y':0,'Left_ankle:Z':0,'Left_ankle:TrueDistance':0}, ignore_index=True)
"""
def detectRect(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,2)
    contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('Rectangle',thresh)
    for contour in contours:
        if(cv2.contourArea(contour)>700):
            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
            if(len(approx)==4):
                x,y,w,h = cv2.boundingRect(approx)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 1)
                #cv2.imshow('Rectangle', img)
"""        

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

def render_result(skeletons, color_img, depth_img, intr, confidence_threshold):
    global df
    #depth_frame.__class__ = rs.pyrealsense2.depth_frame
    white = np.zeros([640,800,3],dtype=np.uint8)
    white.fill(255)
    skeleton_color = (0, 140, 255)
    #print(f"#Skeletons in frame : {len(skeletons)}")
    if len(skeletons) == 1:
        for index, skeleton in enumerate(skeletons):
            x1,y1,z1,true_dist1 = None,None,None,None
            x2,y2,z2,true_dist2 = None,None,None,None
            x3,y3,z3,true_dist3 = None,None,None,None
            x4,y4,z4,true_dist4 = None,None,None,None
            x5,y5,z5,true_dist5 = None,None,None,None
            x6,y6,z6,true_dist6 = None,None,None,None
            x7,y7,z7,true_dist7 = None,None,None,None
            x8,y8,z8,true_dist8 = None,None,None,None
            x9,y9,z9,true_dist9 = None,None,None,None
            x10,y10,z10,true_dist10 = None,None,None,None
            x11,y11,z11,true_dist11 = None,None,None,None
            x12,y12,z12,true_dist12 = None,None,None,None
            x13,y13,z13,true_dist13 = None,None,None,None
            x14,y14,z14,true_dist14 = None,None,None,None
            joint_locations,joint_distances = get_valid_coordinates(skeleton, depth_img, confidence_threshold)
            for joint,coordinate in joint_locations.items():
                if joint == 'Right_ear' or joint == 'Left_ear' or joint == 'Right_eye' or joint == 'Left_eye':
                    continue
                elif(joint == 'Neck'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    x1,y1,z1 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist1 = math.sqrt((x1**2)+(y1**2)+(z1**2))
                    cv2.putText(white,"xyz = {0:.4},{1:.4},{2:.4}".format(x1,y1,z1),(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
                    cv2.putText(white,"trueDist = {0:.4}".format(true_dist1),(20,120), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,154),2,cv2.LINE_AA)
                    cv2.putText(white,"Difference = {0:.5}".format((true_dist1-z1)),(20,230), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,154),2,cv2.LINE_AA)
                elif(joint == 'Nose'):
                    x2,y2,z2 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist2 = math.sqrt((x2**2)+(y2**2)+(z2**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Right_shoulder'):
                    x3,y3,z3 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist3 = math.sqrt((x3**2)+(y3**2)+(z3**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Right_elbow'):
                    x4,y4,z4 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist4 = math.sqrt((x4**2)+(y4**2)+(z4**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Right_wrist'):
                    x5,y5,z5 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist5 = math.sqrt((x5**2)+(y5**2)+(z5**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Left_shoulder'):
                    x6,y6,z6 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist6 = math.sqrt((x6**2)+(y6**2)+(z6**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Left_elbow'):
                    x7,y7,z7 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist7 = math.sqrt((x7**2)+(y7**2)+(z7**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Left_wrist'):
                    x8,y8,z8 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist8 = math.sqrt((x8**2)+(y8**2)+(z8**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Right_hip'):
                    x9,y9,z9 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist9 = math.sqrt((x9**2)+(y9**2)+(z9**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Right_knee'):
                    x10,y10,z10 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist10 = math.sqrt((x10**2)+(y10**2)+(z10**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Right_ankle'):
                    x11,y11,z11 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist11 = math.sqrt((x11**2)+(y11**2)+(z11**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Left_hip'):
                    x12,y12,z12 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist12 = math.sqrt((x12**2)+(y12**2)+(z12**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Left_knee'):
                    x13,y13,z13 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist13 = math.sqrt((x13**2)+(y13**2)+(z13**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
                elif(joint == 'Left_ankle'):
                    x14,y14,z14 = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist14 = math.sqrt((x14**2)+(y14**2)+(z14**2))
                    cv2.circle(color_img, coordinate, radius=5, color=(34, 240, 25), thickness=-1)
            
            df = df.append({'Nose:X':x1,'Nose:Y':y1,'Nose:Z':z1,'Nose:TrueDistance':true_dist1,
                'Neck:X':x2,'Neck:Y':y2,'Neck:Z':z2,'Neck:TrueDistance':true_dist2,
                'Right_shoulder:X':x3,'Right_shoulder:Y':y3,'Right_shoulder:Z':z3,'Right_shoulder:TrueDistance':true_dist3,
                'Right_elbow:X':x4,'Right_elbow:Y':y4,'Right_elbow:Z':z4,'Right_elbow:TrueDistance':true_dist4,
                'Right_wrist:X':x5,'Right_wrist:Y':y5,'Right_wrist:Z':z5,'Right_wrist:TrueDistance':true_dist5,
                'Left_shoulder:X':x6,'Left_shoulder:Y':y6,'Left_shoulder:Z':z6,'Left_shoulder:TrueDistance':true_dist6,
                'Left_elbow:X':x7,'Left_elbow:Y':y7,'Left_elbow:Z':z7,'Left_elbow:TrueDistance':true_dist7,
                'Left_wrist:X':x8,'Left_wrist:Y':y8,'Left_wrist:Z':z8,'Left_wrist:TrueDistance':true_dist8,
                'Right_hip:X':x9,'Right_hip:Y':y9,'Right_hip:Z':z9,'Right_hip:TrueDistance':true_dist9,
                'Right_knee:X':x10,'Right_knee:Y':y10,'Right_knee:Z':z10,'Right_knee:TrueDistance':true_dist10,
                'Right_ankle:X':x11,'Right_ankle:Y':y11,'Right_ankle:Z':z11,'Right_ankle:TrueDistance':true_dist11,
                'Left_hip:X':x12,'Left_hip:Y':y12,'Left_hip:Z':z12,'Left_hip:TrueDistance':true_dist12,
                'Left_knee:X':x13,'Left_knee:Y':y13,'Left_knee:Z':z13,'Left_knee:TrueDistance':true_dist13,
                'Left_ankle:X':x14,'Left_ankle:Y':y14,'Left_ankle:Z':z14,'Left_ankle:TrueDistance':true_dist14}, ignore_index=True)
            
            #print(message)
            cv2.imshow('Skeleton', color_img)    
            cv2.imshow('Output',white) 
            #out.write(color_img)
    else:
        cv2.imshow('Skeleton', color_img)  
        cv2.imshow('Output',white)   
        #out.write(color_img)

while True:
    count = count+1
    frame = pipeline.wait_for_frames()
    align = rs.align(rs.stream.color)
    aligned_frame = align.process(frame)
    depth_frame = aligned_frame.get_depth_frame()
    color_frame = aligned_frame.get_color_frame()
    spatial_depth = spatial.process(depth_frame)
    #decimated_depth = decimation.process(depth_frame)
    prof = spatial_depth.get_profile()
    video_prof = prof.as_video_stream_profile()
    intrinsics = video_prof.get_intrinsics()
    #filled_depth = hole_filling.process(filtered_depth)
    #depth_image = np.asanyarray(depth_frame.get_data())
    depth_image_spatial = np.asanyarray(spatial_depth.get_data())
    #depth_image_decimated = np.asanyarray(decimated_depth.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    #color_image = cv2.resize(color_image, (int(color_image.shape[1]/3), int(color_image.shape[0]/3)), interpolation = cv2.INTER_CUBIC)
    skeletons = api.estimate_keypoints(color_image, 256) 
    #render_result(skeletons, color_image, depth_image, intrinsics, 0.6)
    render_result(skeletons, color_image,depth_image_spatial, intrinsics, 0.6) 
    #detectRect(color_image)
    cv2.namedWindow('Skeleton', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('Output', cv2.WINDOW_AUTOSIZE)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyWindow('Skeleton')
        break
pipeline.stop()
df = df.tail(-1)
df.to_csv ('/home/kathir/Desktop/Data/spatial_glare.csv', index = False, header=True)
os.system('cls||clear')
print(count)