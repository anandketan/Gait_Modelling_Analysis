from cv2 import aruco as aruco
import cv2
import numpy as np
import pyrealsense2 as rs

id_to_find = 69
marker_size = 15

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()   

depth = np.array([0.0,0.0,0.0,0.0],dtype=np.float32)
coordinates = []
print(depth.shape)

for x in range(5):
  pipeline.wait_for_frames()

camera_matrix = np.loadtxt('camera calibration.txt',delimiter=',')
camera_distortion = np.loadtxt('distortion.txt',delimiter=',')

R_flip = np.zeros((3,3),dtype=np.float32)
R_flip[0,0] = 1.0
R_flip[1,1] = -1.0
R_flip[2,2] = -1.0

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)
#aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters_create()


while True:
    frame = pipeline.wait_for_frames()
    align = rs.align(rs.stream.color)
    aligned_frame = align.process(frame)
    depth_frame = aligned_frame.get_depth_frame()
    color_frame = aligned_frame.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())
    gray = cv2.cvtColor(color_image,cv2.COLOR_BGR2GRAY)
    corners,ids,rejected = aruco.detectMarkers(image=gray,dictionary=aruco_dict, parameters=parameters,cameraMatrix=camera_matrix, distCoeff = camera_distortion)
    for corner in corners:
        for i in range (4):
            c = tuple(map(int, corner[0][i]))
            coordinates.append(c)
            x,y = c
            dist= depth_image[y,x]*depth_scale
            depth[i] = dist
            i+=1
    
    print(depth)
    print(coordinates)
    coordinates.clear()
    ids = np.array(ids)
    
    if ids!=None and (ids[0] == id_to_find).any():
        ret = aruco.estimatePoseSingleMarkers(corners,marker_size,camera_matrix,camera_distortion)
        rvec,tvec = ret[0][0,0:],ret[1][0,0:]
        aruco.drawDetectedMarkers(color_image,corners)
        #aruco.drawAxis(color_image,camera_matrix,camera_distortion,rvec,tvec,10)

    cv2.imshow("Floor", color_image)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
  
cv2.destroyAllWindows()