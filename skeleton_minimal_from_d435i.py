## License: ?
## Copyright(c) Cubemos GmBH. All Rights Reserved.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

import time
import os
import cv2
import numpy as np
import pyrealsense2 as rs
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice #refer to cubmos documentation for installation
from cubemos.skeletontracking.native_wrapper import Api #refer to cubmos documentation for installation
import open3d as o3d

joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license") #"LOCALAPPDATA" in place of "HOME" for windows 10


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
"""
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('skeleton_coordinates.avi', fourcc, 15.0, (640, 480))
"""
api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

pcd = o3d.geometry.PointCloud()

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

def get_valid_coordinates(skeleton, depth, confidence_threshold):
    result_coordinate = {}
    result_distance = {}
    for i in range (len(skeleton.joints)):
        if skeleton.confidences[i] >= confidence_threshold:
            if skeleton.joints[i][0] >= 0 and skeleton.joints[i][1] >= 0:
                result_coordinate[joints[i]] = tuple(map(int, skeleton.joints[i]))
                dist,_,_,_ = cv2.mean((depth[result_coordinate[joints[i]][0]-1:result_coordinate[joints[i]][0]+1,result_coordinate[joints[i]][1]-1:result_coordinate[joints[i]][1]+1].astype(float))*depth_scale)
                result_distance[joints[i]] = dist
    return result_coordinate,result_distance

def convert_depth_to_phys_coord_using_realsense(intrin,x, y, depth):  
    result = rs.rs2_deproject_pixel_to_point(intrin, [x, y], depth)  
    #result[0]: right (x), result[1]: down (y), result[2]: forward (z) from camera POV
    return result[2], -result[0], -result[1]

def render_result(skeletons, color_img, depth_img, intr, confidence_threshold):
    i=1
    skeleton_color = (100, 254, 213)
    if len(skeletons) == 1:
        A = np.array([[0,0,0]])
        for index, skeleton in enumerate(skeletons):
            joint_locations,joint_distances = get_valid_coordinates(skeleton, depth_img, confidence_threshold)
            #print ("Resultant dictionary is : " +  str(joint_locations))
            for joint,coordinate in joint_locations.items():
                if joint == 'Right_ear' or joint == 'Left_ear' or joint == 'Right_eye' or joint == 'Left_eye':
                    continue
                else:
                    x,y,z = convert_depth_to_phys_coord_using_realsense(intr, coordinate[0], coordinate[1], joint_distances[joint])
                    A = np.append(A,[np.array([x,y,z])],axis=0)
                    cv2.circle(color_img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                    cv2.putText(color_img,"x={0} y={1} z={2}".format(x,y,z),coordinate, cv2.FONT_HERSHEY_SIMPLEX, 0.5,(165,44,59),2,cv2.LINE_AA)
            cv2.imshow('Skeleton', color_img)    
        #out.write(color_img)
        #print(A.shape)
        #A = o3d.utility.Vector3dVector(A)
        #geometry.points = o3d.utility.Vector3dVector(A)
        #vis.add_geometry(geometry)
        #vis.poll_events()
        #vis.update_renderer()
        #if key & 0xFF == ord('q') or key == 27:
            #vis.destroy_window()
        #print(pcd.points)
        #o3d.io.write_point_cloud("./data.ply", pcd)
        #o3d.visualization.draw_geometries([pcd])

        
    
"""
vis = o3d.visualization.Visualizer()
vis.create_window()
geometry = o3d.geometry.PointCloud()
"""
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
        #vis.destroy_window()
        break
#vis.destroy_window()
pipeline.stop()
