import math
import cmath
import numpy as np
import pandas as pd
import pickle
import pyrealsense2 as rs
import cv2

def calculateAngleFromSlope(a, b):
    #gives angle from slope wrt x-axis
    if a[0]-b[0]!=0:
        rad = math.atan((a[1]-b[1])/(a[0]-b[0]))
    else:
        rad = math.pi/2 
    deg = rad * 180 / math.pi
    if deg<0:
        deg = 180 + deg
    return deg

def calculateAngle2d(a, b, c):
    #gives 2d angle of 2 vectors represented by end points
    x1, y1 = a 
    x2, y2 = b #midpoint
    x3, y3 = c               
    ABx = x1 - x2
    ABy = y1 - y2
    BCx = x3 - x2
    BCy = y3 - y2
    dotProduct = ABx * BCx + ABy * BCy
    # print(dotProduct)
    magnitudeAB = math.sqrt(ABx * ABx + ABy * ABy)
    # print(magnitudeAB)
    magnitudeBC = math.sqrt(BCx * BCx + BCy * BCy)
    # print(magnitudeBC)
    angle = math.acos(dotProduct/(magnitudeAB*magnitudeBC))
    angle = (angle * 180) / math.pi
    # return(round(abs(angle), 4))
    return angle

def calculateAngle3d(p1, p2, p3):
    #gives 3d angle of 2 vectors represented by end points   
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    x3, y3, z3 = p3                
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

def calculateDistance(p1, p2):
    #gives distance between 2 points in 3d or 2d
    p1 = np.array(p1)
    p2 = np.array(p2)
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def get_init_pos_from_pkl(filepath):
    #reads initial position from store pickle file
    with open(filepath, 'rb') as file:
            init_pos = pickle.load(file)
    return init_pos

def get_init_pos_from_csv(filepath, type, by):
    #gets initial position from stored csv file
    joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']
    df = pd.read_csv(filepath)
    print(len(df))
    if type == 'position3d':
        init_pos = {key: (0,0,0) for key in joints}
        for i in joints:
            try:
                if by == 'mean':
                    init_pos[i] = (df['{}X'.format(i)].mean(), df['{}Y'.format(i)].mean(), df['{}Z'.format(i)].mean())
                elif by == 'median':
                    init_pos[i] = (df['{}X'.format(i)].median(), df['{}Y'.format(i)].median(), df['{}Z'.format(i)].median())
            except:
                init_pos[i] = (0,0,0)
    elif type == 'position2d':
        init_pos = {key: (0,0) for key in joints}
        for i in joints:
            try:
                if by == 'mean':
                    init_pos[i] = (round(df['{}X'.format(i)].mean()), round(df['{}Y'.format(i)].mean()))
                elif by == 'median':
                    init_pos[i] = (round(df['{}X'.format(i)].median()), round(df['{}Y'.format(i)].median()))
            except:
                init_pos[i] = (0,0)
    elif type == 'distance2d':
        init_pos = {key: 0 for key in joints}
        for i in joints:
            try:
                if by == 'mean':
                    init_pos[i] = df[i].mean()
                elif by == 'median':
                    init_pos[i] = df[i].median()
            except:
                init_pos[i] = 0
    return init_pos

def save_positional_to_csv(position_data3d, filenamepos3d, position_data2d, filenamepos2d, distance_data2d, filenamedis2d):
    #save all positional data to csv files
    joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']
    df = pd.DataFrame(position_data3d ,columns=joints)
    df2 = pd.DataFrame(position_data2d ,columns=joints)
    df3 = pd.DataFrame(distance_data2d ,columns=joints)
    old_cols = df.columns
    for i in old_cols:
        df[['{}X'.format(i), '{}Y'.format(i), '{}Z'.format(i)]] = pd.DataFrame(df[i].tolist(), index=df.index)
        df2[['{}X'.format(i), '{}Y'.format(i)]] = pd.DataFrame(df2[i].tolist(), index=df.index)
    df.drop(columns=old_cols, inplace=True)
    df2.drop(columns=old_cols, inplace=True)
    df.replace(0, np.nan, inplace=True)
    df2.replace(0, np.nan, inplace=True)
    df3.replace(0, np.nan, inplace=True)
    df.to_csv(filenamepos3d)
    df2.to_csv(filenamepos2d)
    df3.to_csv(filenamedis2d)

def convert_depth_to_phys_coord_using_realsense(intrin,x, y, depth):  
    result = rs.rs2_deproject_pixel_to_point(intrin, [x, y], depth)  
    #result[0]: right (x), result[1]: down (y), result[2]: forward (z) from camera POV
    return result[0], result[1], result[2]

def get_valid_coordinates(skeleton, depth, confidence_threshold, depth_scale):
    joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']
    result_coordinate = {}
    result_distance = {}
    for i in range (len(skeleton.joints)):
        if skeleton.confidences[i] >= confidence_threshold:
            if skeleton.joints[i][0] >= 0 and skeleton.joints[i][1] >= 0:
                result_coordinate[joints[i]] = tuple(map(int, skeleton.joints[i]))
                dist,_,_,_ = cv2.mean((depth[result_coordinate[joints[i]][1]-3:result_coordinate[joints[i]][1]+3,result_coordinate[joints[i]][0]-3:result_coordinate[joints[i]][0]+3].astype(float))*depth_scale)
                result_distance[joints[i]] = dist
    return result_coordinate,result_distance

def sway_string_generator(sway_angle, right_limit, left_limit, right_limit_extreme, left_limit_extreme):
    if(sway_angle>=right_limit and sway_angle<=left_limit):
        sideways = ""
    if sway_angle < right_limit:
        if sway_angle < right_limit_extreme:
            sideways = "R2"
        else:
            sideways = "R1"
    elif sway_angle > left_limit:
        if sway_angle < left_limit_extreme:
            sideways = "L1"
        else:
            sideways = "L2"
    return sideways

def forwards_string_generator(forward_angle, forward_limit, forward_limit_extreme, reverse_limit = 180):
    if forward_angle < forward_limit:
        if forward_angle < forward_limit_extreme:
            forwards = "F2"
        else:
            forwards = "F1"
    elif forward_angle > reverse_limit:
        forwards = "Re"
    return forwards

def direction_string_generator(forwards, sideways):
    if forwards != "" and sideways != "":
        direction = "{}-{}".format(forwards, sideways)
    else:
        if forwards != "":
            direction = forwards
        else:
            direction = sideways
    return direction

def is_reach_out_right(coordinates2d):
    flag = False
    limit = 75
    try:
        if calculateAngle2d(coordinates2d['Right_elbow'], coordinates2d['Right_shoulder'], coordinates2d['Right_hip']) >= limit:
            flag = True
    except:
        pass
    return flag

def is_reach_out_left(coordinates2d):
    flag = False
    limit = 75
    try:
        if calculateAngle2d(coordinates2d['Left_elbow'], coordinates2d['Left_shoulder'], coordinates2d['Left_hip']) >= limit:
            flag = True
    except:
        pass
    return flag