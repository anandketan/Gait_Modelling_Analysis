import cv2
import numpy as np
import pyrealsense2 as rs
import pandas as pd
import os
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice
from cubemos.skeletontracking.native_wrapper import Api 

joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license")

api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 15)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

for x in range(5):
  pipeline.wait_for_frames()

spatial = rs.spatial_filter()
spatial.set_option(rs.option.filter_magnitude, 5)
spatial.set_option(rs.option.filter_smooth_alpha, 1)
spatial.set_option(rs.option.filter_smooth_delta, 50)
hole_filling = rs.hole_filling_filter()

df = pd.DataFrame(columns = ['Raw_with_holes', 'Spatial_without_holes'])
df = df.append({'Raw_with_holes' : 0 ,'Spatial_without_holes' : 0}, ignore_index=True)
print(df)
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
    print("x={},y={}".format(x,y))
    result = rs.rs2_deproject_pixel_to_point(intrin, [x, y], depth)  
    #result[0]: right (x), result[1]: down (y), result[2]: forward (z) from camera POV
    return result[0], result[1], result[2]

def render_result(skeletons, color_img, depth_img,depth_frame, intr, confidence_threshold):
    depth_frame.__class__ = rs.pyrealsense2.depth_frame
    white = np.zeros([640,800,3],dtype=np.uint8)
    white.fill(255)
    skeleton_color = (0, 140, 255)
    #print(f"#Skeletons in frame : {len(skeletons)}")
    if len(skeletons) == 1:
        for index, skeleton in enumerate(skeletons):
            joint_locations,joint_distances = get_valid_coordinates(skeleton, depth_img, confidence_threshold)
            for joint,coordinate in joint_locations.items():
                #x,y,z = 0,0,0
                if joint == 'Right_ear' or joint == 'Left_ear' or joint == 'Right_eye' or joint == 'Left_eye':
                    continue
                elif(joint == 'Nose'):
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    true_dist = depth_frame.get_distance(coordinate[0], coordinate[1])
                    cv2.putText(white,"Nose_xyz = {0:.4},{1:.4},{2:.4}".format(x,y,z),(20,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
                    cv2.putText(white,"Nose_trueDist = {0:.4}".format(true_dist),(20,120), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,154),2,cv2.LINE_AA)
                    cv2.putText(white,"Nose_Difference = {0:.5}".format((true_dist-z)),(20,230), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,154),2,cv2.LINE_AA)
                else:
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
            
            
            #print(message)
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
    filtered_depth = spatial.process(depth_frame)
    #filled_depth = hole_filling.process(filtered_depth)
    depth_image = np.asanyarray(depth_frame.get_data())
    depth_image_spa = np.asanyarray(filtered_depth.get_data())
    #df = df.append({'Raw_with_holes' : dist*100.0 ,'Spatial_without_holes' : dist_spa*100.0}, ignore_index=True)
    color_image = np.asanyarray(color_frame.get_data())
    skeletons = api.estimate_keypoints(color_image, 192) 
    #render_result(skeletons, color_image, depth_image, intrinsics, 0.6)
    render_result(skeletons, color_image, depth_image_spa,filtered_depth, intrinsics, 0.6)
    #detectRect(color_image)
    cv2.namedWindow('Skeleton', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow('Output', cv2.WINDOW_AUTOSIZE)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyWindow('Skeleton')
        break
pipeline.stop()

df.to_csv ('neck_dist.csv', index = False, header=True)
