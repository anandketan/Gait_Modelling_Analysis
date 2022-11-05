from math import atan2
import pandas as pd
import numpy as np
import pptk
import open3d as o3d
from open3d import *
import time
import math

# joints = ['Nose','Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
#         'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
#         'Left_knee','Left_ankle','Right_eye','Left_eye','Right_ear','Left_ear']
joints = ['Neck','Right_shoulder','Right_elbow','Right_wrist','Left_shoulder',
        'Left_elbow','Left_wrist','Right_hip','Right_knee','Right_ankle','Left_hip',
        'Left_knee','Left_ankle','Camera']

# lines = [[0,14], [0,15], [14,16], [15,17], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [2,8], [8,9], [9,10], [5,11], [11,12], [12,13]]
lines = [[0,1], [1,2], [2,3], [0,4], [4,5], [5,6], [1,7], [7,8], [8,9], [4,10], [10,11], [11,12]]
#random coordinates from a previous experiment. Setting everything to zero doesn't seem to work
coords3d=  {'Neck': (0.19302140176296234, 0.04428612068295479, 1.3540000915527344),
'Right_shoulder': (0.03314350172877312, 0.03538845479488373, 1.3572778701782227),
'Right_elbow': (-0.04068613797426224, 0.24781912565231323, 1.3216111660003662),
'Right_wrist': (-0.08127983659505844, 0.29209014773368835, 1.0844722986221313),
'Left_shoulder': (0.34972065687179565, 0.04387727379798889, 1.3415000438690186),
'Left_elbow': (0.44440022110939026, 0.25280147790908813, 1.3021111488342285),
'Left_wrist': (0.4161774814128876, 0.2813136875629425, 1.0985833406448364),
'Right_hip': (0,0,0),
'Right_knee': (0,0,0),
'Right_ankle': (0,0,0),
'Left_hip': (0,0,0),
'Left_knee': (0,0,0),
'Left_ankle': (0,0,0),
'Right_eye': (0.17547458410263062, -0.14218689501285553, 1.280500054359436),
'Left_eye': (0.22900129854679108, -0.13275755941867828, 1.2715556621551514),
'Right_ear': (0.12736432254314423, -0.143180713057518, 1.3713889122009277),
'Left_ear': (0.28060203790664673, -0.13001656532287598, 1.329805612564087),
'Camera': (0,0,0)}

df = pd.DataFrame.from_dict(coords3d, orient="index", columns=["X", "Y", "Z"])
x = df.to_numpy()


# o3d.visualization.draw_geometries([pcd])
points = x

df2 = pd.read_csv("C:\\Users\\Testing\\Downloads\\reachstepout_position3d_new.csv")
df2.drop(columns = ['Unnamed: 0'], inplace = True)
for i in joints[:-1]:
    df2['{}coords'.format(i)] = list(zip(df2['{}X'.format(i)],df2['{}Y'.format(i)],df2['{}Z'.format(i)]))

origin = [(df2['Left_hipX'].mean() + df2['Right_hipX'].mean())/2,
        (df2['Left_hipY'].mean() + df2['Right_hipY'].mean())/2,
        (df2['Left_hipZ'].mean() + df2['Right_hipZ'].mean())/2]

print(origin)

left_hip = (df2['Left_hipX'].mean(), df2['Left_hipY'].mean(), df2['Left_hipZ'].mean())
right_hip = (df2['Right_hipX'].mean(), df2['Right_hipY'].mean(), df2['Right_hipZ'].mean())

left_hip_new = tuple(map(lambda i, j: i - j, left_hip, right_hip))
right_hip_new = tuple(map(lambda i, j: i - j, right_hip, right_hip))

new_points = np.array([list(left_hip_new),list(right_hip_new)])
new_points[0,1] = 0.0
# new_points = np.array([list(left_hip),list(right_hip)])

print("Before", left_hip, right_hip)
print("After", new_points)

print(math.degrees(math.atan(new_points[0,2]/new_points[0,0])))

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
colors = [[1, 0, 0] for i in range(len(lines))]
line_set = o3d.geometry.LineSet()
line_set.points = o3d.utility.Vector3dVector(points)
line_set.lines = o3d.utility.Vector2iVector(lines)
line_set.colors = o3d.utility.Vector3dVector(colors)
line_set2 = o3d.geometry.LineSet()
line_set2.points = o3d.utility.Vector3dVector(new_points)
line_set2.lines = o3d.utility.Vector2iVector([[0,1]])
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 0.6, origin = origin)
R = mesh_frame.get_rotation_matrix_from_xyz((0, np.pi - math.atan(new_points[0,2]/new_points[0,0]), 0))
# R = np.array([[-1, 0 , 0], [0, -1, 0], [0, 0, -1]])
# print(R)
mesh_frame.rotate(R, center = origin)
print(o3d.geometry.TriangleMesh.get_rotation_matrix_from_axis_angle([0,0,0]))
mesh_frame2 = o3d.geometry.TriangleMesh.create_coordinate_frame(size = 0.6, origin = [0,0,0])
vis = o3d.visualization.Visualizer()
vis.create_window(width=1280, height=720)
vis.add_geometry(line_set)
vis.add_geometry(line_set2)
vis.add_geometry(pcd)
vis.add_geometry(mesh_frame)
vis.add_geometry(mesh_frame2)
# opt = vis.get_render_option()
# opt.show_coordinate_frame = True
# opt.background_color = np.asarray([0.5, 0.5, 0.5])
# ctr = vis.get_view_control()
# parameters = o3d.io.read_pinhole_camera_parameters("ScreenCamera_2021-07-30-12-30-12.json")
# ctr.convert_from_pinhole_camera_parameters(parameters)

# df2 = pd.read_csv("C:\\Users\\Testing\\Downloads\\reachstepout_position3d.csv")
# df2.drop(columns = ['Unnamed: 0'], inplace = True)
# for i in joints[:-1]:
#     df2['{}coords'.format(i)] = list(zip(df2['{}X'.format(i)],df2['{}Y'.format(i)],df2['{}Z'.format(i)]))
# df2.drop(columns=[i for i in joints])
# print(df2.columns[54:])
print(len(df2))
i=10

while i<len(df2):
    x = df2.iloc[i, 54:].to_numpy()
    print(i)
    points = x
    i+=1
    line_set.points = o3d.utility.Vector3dVector(points)
    pcd.points = o3d.utility.Vector3dVector(points)
    vis.update_geometry(line_set)
    vis.update_geometry(pcd)
    vis.update_renderer()
    vis.poll_events()
    time.sleep(1/30)

# forward_angle = calculateAngle(x_left_hip,y_left_hip,z_left_hip,x_right_hip,y_right_hip,z_right_hip)