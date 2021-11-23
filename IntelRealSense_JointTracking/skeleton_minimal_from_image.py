## License: ?
## Copyright(c) Cubemos GmBH. All Rights Reserved.

import os
import cv2
import numpy as np
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice #refer to cubmos documentation for installation
from cubemos.skeletontracking.native_wrapper import Api #refer to cubmos documentation for installation

"""
DO NOT DELETE THIS COMMENT!!! MIGHT NEED FOR FUTURE REFERENCES.
(0, 14),
    (14, 16),
    (0, 15),
    (15, 17)
"""
keypoint_ids = [
    (1, 2),
    (1, 5),
    (2, 3),
    (3, 4),
    (5, 6),
    (6, 7),
    (1, 8),
    (8, 9),
    (9, 10),
    (1, 11),
    (11, 12),
    (12, 13),
    (1, 0)
]


joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']
        
def get_valid_coordinates(skeleton, confidence_threshold):
    coordinates = [
        (tuple(map(int, skeleton.joints[i])))
        for i in range (len(skeleton.joints))
        if skeleton.confidences[i] >= confidence_threshold
    ]
    valid_coordinates = [
        coordinate
        for coordinate in coordinates
        if coordinate[0] >= 0 and coordinate[1] >= 0 
    ]
    result = {joints[i]: valid_coordinates[i] for i in range(len(joints))}
    del result['Right_eye']
    del result['Left_eye']
    del result['Right_ear']
    del result['Left_ear']

    return result

def get_valid_keypoints(keypoint_ids, skeleton, confidence_threshold):
    keypoints = [
        (tuple(map(int, skeleton.joints[i])), tuple(map(int, skeleton.joints[v])))
        for (i, v) in keypoint_ids
        if skeleton.confidences[i] >= confidence_threshold
        and skeleton.confidences[v] >= confidence_threshold
    ]
    valid_keypoints = [
        keypoint
        for keypoint in keypoints
        if keypoint[0][0] >= 0 and keypoint[0][1] >= 0 and keypoint[1][0] >= 0 and keypoint[1][1] >= 0
    ]
    return valid_keypoints


def render_result(skeletons, img, confidence_threshold):
    skeleton_color = (100, 254, 213)
    for index, skeleton in enumerate(skeletons):
        print(len(skeleton.joints))
        joint_locations = get_valid_coordinates(skeleton, confidence_threshold)
        keypoints = get_valid_keypoints(keypoint_ids, skeleton, confidence_threshold)
        for keypoint in keypoints:
            cv2.line(white, keypoint[0], keypoint[1], skeleton_color, thickness=2, lineType=cv2.LINE_AA)
        print ("Resultant dictionary is : " +  str(joint_locations))
        for joint,coordinate in joint_locations.items():
            cv2.circle(white, coordinate, radius=5, color=(0,69,255), thickness=-1)
            if joint == 'Neck':
                cv2.putText(white,'Neck',(coordinate[0]+15,coordinate[1]-30), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(77,44,159),1,cv2.LINE_AA)
                cv2.putText(white,'(Xi = -0.2, Yi = -0.64, Zi = 2.93)',(coordinate[0]+3,coordinate[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(160,44,59),1,cv2.LINE_AA)
            if joint == 'Left_elbow':
                cv2.putText(white,joint,(coordinate[0]+15,coordinate[1]-25-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(77,44,159),1,cv2.LINE_AA)
                cv2.putText(white,'(Xi = 0.31, Yi = -0.38, Zi = 3.2)',(coordinate[0]+3,coordinate[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(160,44,59),1,cv2.LINE_AA)
            if joint == 'Right_wrist':
                cv2.putText(white,joint,(coordinate[0]+15,coordinate[1]-25-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(77,44,159),1,cv2.LINE_AA)
                cv2.putText(white,'(Xi = -0.52, Yi = -0.41, Zi = 3.03)',(coordinate[0]+3,coordinate[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(160,44,59),1,cv2.LINE_AA)
            if joint == 'Left_knee':
                cv2.putText(white,joint,(coordinate[0]+15,coordinate[1]-25-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(77,44,159),1,cv2.LINE_AA)
                cv2.putText(white,'(Xi = 0.27, Yi = 0.59, Zi = 3.5)',(coordinate[0]+3,coordinate[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(160,44,59),1,cv2.LINE_AA)
            if joint == 'Right_ankle':
                cv2.putText(white,joint,(coordinate[0]+15,coordinate[1]-25-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(77,44,159),1,cv2.LINE_AA)
                cv2.putText(white,'(Xi = -0.36, Yi = -0.77, Zi = 3.47)',(coordinate[0]+3,coordinate[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(160,44,59),1,cv2.LINE_AA)
    cv2.imshow('Skeleton', white)
    

def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license") #"LOCALAPPDATA" in place of "HOME" for windows 10


#Read an RGB image of any size
img = cv2.imread('/opt/cubemos/skeleton_tracking/samples/res/images/me.jpeg') #Change the location to the image of your choice

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

resize = ResizeWithAspectRatio(img, height=857)
white = np.zeros([resize.shape[0]+100,resize.shape[1]+300,3],dtype=np.uint8)
white.fill(255)
#initialize the api with a valid license key in default_license_dir()
api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)
#perform inference
skeletons = api.estimate_keypoints(resize, 256) 
print("Detected skeletons: ", len(skeletons))
cv2.namedWindow('Skeleton', cv2.WINDOW_AUTOSIZE)
render_result(skeletons, resize, 0.5)
key = cv2.waitKey(0)
if key & 0xFF == ord('q') or key == 27:
    cv2.destroyAllWindows()