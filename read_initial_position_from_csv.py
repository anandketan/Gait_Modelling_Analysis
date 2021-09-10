import pandas as pd
import numpy as np
import math
import cmath
import pickle

joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']

def calculateAngle2d(a, b, c):   
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
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

def get_init_pos_from_pkl():
    with open('initial3d_by_mean.pkl', 'rb') as file:
            init_pos3d = pickle.load(file)
    with open('initial3d_by_median.pkl', 'rb') as file:
            init_pos3d_median = pickle.load(file)
    with open('initial2d_by_mean.pkl', 'rb') as file:
            init_pos2d = pickle.load(file)
    with open('initial2d_by_median.pkl', 'rb') as file:
            init_pos2d_median = pickle.load(file)
    with open('initial2d_dis_by_mean.pkl', 'rb') as file:
            init_dis2d = pickle.load(file)
    with open('initial2d_dis_by_median.pkl', 'rb') as file:
            init_dis2d_median = pickle.load(file)
    return init_dis2d, init_dis2d_median, init_pos2d, init_pos2d_median, init_pos3d, init_pos3d_median
    


def get_init_pos_from_csv():
    df = pd.read_csv("C:\\Users\\Testing\\Downloads\\position3d.csv")
    df2 = pd.read_csv("C:\\Users\\Testing\\Downloads\\position2d.csv")
    df3 = pd.read_csv("C:\\Users\\Testing\\Downloads\\distance2d.csv")
    init_pos3d = {key: (0,0,0) for key in joints}
    init_pos3d_median = {key: (0,0,0) for key in joints}
    init_pos2d = {key: (0,0) for key in joints}
    init_pos2d_median = {key: (0,0) for key in joints}
    init_dis2d = {key: 0 for key in joints}
    init_dis2d_median = {key: 0 for key in joints}
    for i in joints:
        try:
            init_pos3d[i] = (df['{}X'.format(i)].mean(), df['{}Y'.format(i)].mean(), df['{}Z'.format(i)].mean())
            init_pos3d_median[i] = (df['{}X'.format(i)].median(), df['{}Y'.format(i)].median(), df['{}Z'.format(i)].median())
        except:
            init_pos3d[i] = (0,0,0)
            init_pos3d_median[i] = (0,0,0)
        try:
            init_pos2d[i] = (round(df2['{}X'.format(i)].mean()), round(df2['{}Y'.format(i)].mean()))
            init_pos2d_median[i] = (round(df2['{}X'.format(i)].median()), round(df2['{}Y'.format(i)].median()))
        except:
            init_pos2d[i] = (0,0)
            init_pos2d_median[i] = (0,0)
        try:
            init_dis2d[i] = df3[i].mean()
            init_dis2d_median[i] = df3[i].median()
        except:
            init_dis2d[i] = 0
            init_dis2d_median[i] = 0
    return init_dis2d, init_dis2d_median, init_pos2d, init_pos2d_median, init_pos3d, init_pos3d_median
# print(init_pos3d)

def find_position_angular_differences(init_dis2d, init_dis2d_median, init_pos2d, init_pos2d_median, init_pos3d, init_pos3d_median):
    reachout3d_df = pd.read_csv("C:\\Users\\Testing\\Downloads\\reachout_position3d.csv")
    reachout2d_df = pd.read_csv("C:\\Users\\Testing\\Downloads\\reachout_position2d.csv")
    right_elbowX_diff = []
    right_elbowY_diff = []
    right_elbowZ_diff = []
    right_hipX_diff = []
    right_hipY_diff = []
    right_hipZ_diff = []
    right_shoulderX_diff = []
    right_shoulderY_diff = []
    right_shoulderZ_diff = []
    shoulder_angle3d = []
    ######################2d##########################
    right_elbowX_diff2d = []
    right_elbowY_diff2d = []
    right_hipX_diff2d = []
    right_hipY_diff2d = []
    right_shoulderX_diff2d = []
    right_shoulderY_diff2d = []
    shoulder_angle2d = []
    for i in reachout3d_df.index:
        p1 = np.array(reachout3d_df.loc[i, ['Right_elbowX', 'Right_elbowY', 'Right_elbowZ']])
        p2 = np.array(reachout3d_df.loc[i, ['Right_shoulderX', 'Right_shoulderY', 'Right_shoulderZ']])
        p3 = np.array(reachout3d_df.loc[i, ['Right_hipX', 'Right_hipY', 'Right_hipZ']]) 
        right_elbowX_diff.append(reachout3d_df.loc[i, 'Right_elbowX'] - init_pos3d['Right_elbow'][0])
        right_elbowY_diff.append(reachout3d_df.loc[i, 'Right_elbowY'] - init_pos3d['Right_elbow'][1])
        right_elbowZ_diff.append(reachout3d_df.loc[i, 'Right_elbowZ'] - init_pos3d['Right_elbow'][2])
        right_hipX_diff.append(reachout3d_df.loc[i, 'Right_hipX'] - init_pos3d['Right_hip'][0])
        right_hipY_diff.append(reachout3d_df.loc[i, 'Right_hipY'] - init_pos3d['Right_hip'][1])
        right_hipZ_diff.append(reachout3d_df.loc[i, 'Right_hipZ'] - init_pos3d['Right_hip'][2])
        right_shoulderX_diff.append(reachout3d_df.loc[i, 'Right_shoulderX'] - init_pos3d['Right_shoulder'][0])
        right_shoulderY_diff.append(reachout3d_df.loc[i, 'Right_shoulderY'] - init_pos3d['Right_shoulder'][1])
        right_shoulderZ_diff.append(reachout3d_df.loc[i, 'Right_shoulderZ'] - init_pos3d['Right_shoulder'][2])
        shoulder_angle3d.append(calculateAngle3d(p1, p2, p3))
        p1 = np.array(reachout2d_df.loc[i, ['Right_elbowX', 'Right_elbowY']])
        p2 = np.array(reachout2d_df.loc[i, ['Right_shoulderX', 'Right_shoulderY']])
        p3 = np.array(reachout2d_df.loc[i, ['Right_hipX', 'Right_hipY']])
        right_elbowX_diff2d.append(reachout2d_df.loc[i, 'Right_elbowX'] - init_pos2d['Right_elbow'][0])
        right_elbowY_diff2d.append(reachout2d_df.loc[i, 'Right_elbowY'] - init_pos2d['Right_elbow'][1])
        right_hipX_diff2d.append(reachout2d_df.loc[i, 'Right_hipX'] - init_pos2d['Right_hip'][0])
        right_hipY_diff2d.append(reachout2d_df.loc[i, 'Right_hipY'] - init_pos2d['Right_hip'][1])
        right_shoulderX_diff2d.append(reachout2d_df.loc[i, 'Right_shoulderX'] - init_pos2d['Right_shoulder'][0])
        right_shoulderY_diff2d.append(reachout2d_df.loc[i, 'Right_shoulderY'] - init_pos2d['Right_shoulder'][1])
        shoulder_angle2d.append(calculateAngle2d(p1, p2, p3)) 
    # print(max(right_elbowX_diff))
    right_list = list(zip(right_elbowX_diff,right_elbowY_diff,right_elbowZ_diff,right_hipX_diff,right_hipY_diff,right_hipZ_diff,right_shoulderX_diff,right_shoulderY_diff,right_shoulderZ_diff, shoulder_angle3d,
    right_elbowX_diff2d,right_elbowY_diff2d,right_hipX_diff2d,right_hipY_diff2d,right_shoulderX_diff2d, right_shoulderY_diff2d,shoulder_angle2d))
    return right_list


init_dis2d, init_dis2d_median, init_pos2d, init_pos2d_median, init_pos3d, init_pos3d_median = get_init_pos_from_pkl()
print(init_pos3d_median)
# init_dis2d, init_dis2d_median, init_pos2d, init_pos2d_median, init_pos3d, init_pos3d_median = get_init_pos_from_csv()
# right_list = find_position_angular_differences(init_dis2d, init_dis2d_median, init_pos2d, init_pos2d_median, init_pos3d, init_pos3d_median)
# diff_df = pd.DataFrame(right_list, columns=['REX', 'REY', 'REZ', 'RHX', 'RHY', 'RHZ', 'RSX', 'RSY', 'RSZ', 'Angle','RE2dX', 'RE2dY', 'RH2dX', 'RH2dY', 'RS2dX', 'RS2dY', 'Angle2d'])
# diff_df.to_csv("diff_reachout_position3d.csv")

# #############################################
# p1 = np.array(init_pos3d['Right_elbow'])
# p2 = np.array(init_pos3d['Right_shoulder'])
# p3 = np.array(init_pos3d['Right_hip'])
# distance = calculateDistance(p1, p2)
# angle3d = calculateAngle3d(p1, p2, p3)
# p1 = np.array(init_pos2d['Right_elbow'])
# p2 = np.array(init_pos2d['Right_shoulder'])
# p3 = np.array(init_pos2d['Right_hip'])
# angle2d = calculateAngle2d(p1, p2, p3)