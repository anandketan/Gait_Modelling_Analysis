## License: ?
## Copyright(c) Cubemos GmBH. All Rights Reserved.

import os
import cv2
import numpy as np
from cubemos.skeletontracking.core_wrapper import CM_TargetComputeDevice #refer to cubmos documentation for installation
from cubemos.skeletontracking.native_wrapper import Api #refer to cubmos documentation for installation

def default_license_dir():
    return os.path.join(os.environ["HOME"], ".cubemos", "skeleton_tracking", "license") #"LOCALAPPDATA" in place of "HOME" for windows 10


#Read an RGB image of any size
img = cv2.imread('/opt/cubemos/skeleton_tracking/samples/res/images/skeleton_tracking_2.jpg') #Change the location to the image of your choice
#initialize the api with a valid license key in default_license_dir()
api = Api(default_license_dir())
sdk_path = os.environ["CUBEMOS_SKEL_SDK"]
model_path = os.path.join(sdk_path, "models", "skeleton-tracking", "fp32", "skeleton-tracking.cubemos")
api.load_model(CM_TargetComputeDevice.CM_CPU, model_path)
#perform inference
skeletons = api.estimate_keypoints(img, 256) 
print("Detected skeletons: ", len(skeletons))