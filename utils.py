import math
import cmath
import numpy as np
import pandas as pd
import pickle
import pyrealsense2 as rs
import cv2

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