## License: ?
## Copyright(c) Cubemos GmBH. All Rights Reserved.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

import os
import cv2
import numpy as np
import pyrealsense2 as rs
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice #refer to cubmos documentation for installation
from cubemos.skeletontracking.native_wrapper import Api #refer to cubmos documentation for installation

joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

def get_valid_coordinates(skeleton, confidence_threshold):
    result = {}
    for i in range (len(skeleton.joints)):
        if skeleton.confidences[i] >= confidence_threshold:
            if skeleton.joints[i][0] >= 0 and skeleton.joints[i][1] >= 0:
                result[joints[i]] = tuple(map(int, skeleton.joints[i]))
    return result


def render_result(skeletons, img, confidence_threshold):
    skeleton_color = (100, 254, 213)
    for index, skeleton in enumerate(skeletons):
        joint_locations = get_valid_coordinates(skeleton, confidence_threshold)
        #print ("Resultant dictionary is : " +  str(joint_locations))
        for joint,coordinate in joint_locations.items():
            if joint == 'Right_ear' or joint == 'Left_ear' or joint == 'Right_eye' or joint == 'Left_eye':
                continue
            else:
                cv2.circle(img, coordinate, radius=5, color=skeleton_color, thickness=-1)
                cv2.putText(img,joint,coordinate, cv2.FONT_HERSHEY_SIMPLEX, 0.5,(165,44,59),2,cv2.LINE_AA)
    cv2.imshow('Skeleton', img)


def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license") #"LOCALAPPDATA" in place of "HOME" for windows 10

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)

api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)

profile = pipeline.start(config)

while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    skeletons = api.estimate_keypoints(color_image, 256) 
    cv2.namedWindow('Skeleton', cv2.WINDOW_AUTOSIZE)
    render_result(skeletons, color_image, 0.6)
    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

pipeline.stop()
