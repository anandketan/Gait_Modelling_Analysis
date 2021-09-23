from cv2 import aruco as aruco
import cv2
import numpy as np
import pyrealsense2 as rs
import pandas as pd
import datetime

id_to_find = 99
marker_size = 5

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
#config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

profile = pipeline.start(config)
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()   

depth = np.array([0.0,0.0,0.0,0.0],dtype=np.float32)
coordinates = []
df = pd.DataFrame(columns = ['Time_stamp','X','Y'])

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/kathir/Desktop/Data/floor_detect.avi', fourcc, 30.0, (1280, 720))

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
"""
def convert_depth_to_phys_coord_using_realsense(intrin,depth,coordinates):  
    result = []
    #print("x={},y={}".format(x,y))
    for i in range (0,len(depth)):
        re = rs.rs2_deproject_pixel_to_point(intrin, coordinates[i], depth[i])  
        result.append(re)
    #result[0]: right (x), result[1]: down (y), result[2]: forward (z) from camera POV
    return result
k = 0

def equation_plane(x1, y1, z1, x2, y2, z2, x3, y3, z3):
    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)
    print("equation of plane is ",a, "x +",b, "y +",c, "z +",d, "= 0.")
"""
while True:
    frame = pipeline.wait_for_frames()
    #align = rs.align(rs.stream.color)
    #aligned_frame = align.process(frame)
    #depth_frame = aligned_frame.get_depth_frame()
    #prof = depth_frame.get_profile()
    #video_prof = prof.as_video_stream_profile()
    #intrinsics = video_prof.get_intrinsics()
    color_frame = frame.get_color_frame()
    color_image = np.asanyarray(color_frame.get_data())
    #depth_image = np.asanyarray(depth_frame.get_data())
    ct = datetime.datetime.now()
    ts = ct.timestamp()
    gray = cv2.cvtColor(color_image,cv2.COLOR_BGR2GRAY)
    corners,ids,rejected = aruco.detectMarkers(image=gray,dictionary=aruco_dict, parameters=parameters,cameraMatrix=camera_matrix, distCoeff = camera_distortion)
    for corner in corners:
        for i in range (4):
            c = tuple(map(int, corner[0][i]))
            coordinates.append(c)
            #x,y = c
            #dist= depth_image[y,x]*depth_scale
            #depth[i] = dist
            #i+=1
    
    #print(depth)
    

    if len(coordinates) == 4:
        tup = ((coordinates[1][0]+coordinates[3][0])/2,(coordinates[1][1]+coordinates[3][1])/2)
        print(tup)
        out.write(color_image)
        df = df.append({'Time_stamp':ts,'X':tup[0],'Y':tup[1]},ignore_index=True)
    #res = convert_depth_to_phys_coord_using_realsense(intrinsics,depth,coordinates)
    #print(res)
    #if(k>100):
        #equation_plane(res[0][0], res[0][1], res[0][2], res[1][0], res[1][1], res[1][2], res[2][0], res[2][1], res[2][2])
    coordinates.clear()
    ids = np.array(ids)
    
    


    if ids!=None and (ids[0] == id_to_find).any(): #ids!=None and 
        ret = aruco.estimatePoseSingleMarkers(corners,marker_size,camera_matrix,camera_distortion)
        rvec,tvec = ret[0][0,0:],ret[1][0,0:]
        aruco.drawDetectedMarkers(color_image,corners)
        #aruco.drawAxis(color_image,camera_matrix,camera_distortion,rvec,tvec,10)

    cv2.imshow("Floor", color_image)

    # Press Esc key to exit
    if cv2.waitKey(1) == 27:
        break
    

print(df.describe())
df.to_csv ('/home/kathir/Desktop/Data/floor_coordinates.csv', index = False, header=True)

cv2.destroyAllWindows()